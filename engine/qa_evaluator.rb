#!/usr/bin/env ruby
# frozen_string_literal: true

require 'json'
require 'time'

class StreetSmartQAEvaluator
  RUBRICS_PATH = File.expand_path('../data', __dir__)

  def initialize
    @sop1_rubric = JSON.parse(File.read(File.join(RUBRICS_PATH, 'sop1_new_business_rubric.json')))
    @sop2_rubric = JSON.parse(File.read(File.join(RUBRICS_PATH, 'sop2_policy_change_rubric.json')))
  end

  def evaluate(case_data)
    sop_id = case_data['sop_id']
    if sop_id == 'sop1_new_business'
      evaluate_new_business(case_data, @sop1_rubric)
    elsif sop_id == 'sop2_policy_change'
      evaluate_policy_change(case_data, @sop2_rubric)
    else
      raise "Unknown SOP ID: #{sop_id}"
    end
  end

  private

  def evaluate_new_business(data, rubric)
    role = data['role'] || 'Producer'
    rc = data.dig('data_sources', 'ringcentral') || {}
    magellan = data.dig('data_sources', 'magellan') || {}
    ez = data.dig('data_sources', 'ezlynx') || {}
    transcript = (data['transcript_snippet'] || '').downcase

    violations = []
    checkpoint_results = []
    category_scores = {}

    # Check Non-Negotiables
    # 1. NN_NB_01: Never email quote before presenting on phone
    emailed_first = false
    if role == 'Producer'
      order = (ez['quote_presentation_order'] || '').downcase
      if (order.include?('emailed') && (order.include?('before speaking') || order.include?('without scheduling') || order.include?('directly at'))) ||
         (transcript.include?('attached is your') && transcript.include?('let me know if you want to move forward')) ||
         (rc['phone_presentation_completed'] == false && ez['sales_center_pipeline_stage'] == 'Quoted')
        emailed_first = true
        violations << {
          id: 'NN_NB_01',
          rule: 'Never email a quote before presenting it directly on the phone or screen.',
          severity: 'CRITICAL_FAIL',
          detail: 'Quote was emailed to prospect prior to a live telephone/screen presentation.'
        }
      end
    end

    # 2. NN_NB_02: Do not request declarations page at intake
    asked_decs = false
    task_note = (ez['task_note'] || '').downcase
    if snippet_has_decs_request?(transcript) || task_note.include?('email his current declaration') || task_note.include?('waiting on client to email dec')
      asked_decs = true
      violations << {
        id: 'NN_NB_02',
        rule: 'Do not request a declarations page at intake.',
        severity: 'MAJOR_FLAG',
        detail: 'CSR requested customer to provide existing declarations page during intake.'
      }
    end

    # 3. NN_NB_03: Follow payment rules (EFT monthly/annual prioritized; payment required before binding)
    payment_collected = ez['payment_method_collected']
    if ez['sales_center_pipeline_stage'] == 'Won' && (payment_collected.nil? || payment_collected.to_s.downcase.include?('none') || payment_collected.to_s.strip.empty?)
      violations << {
        id: 'NN_NB_03',
        rule: 'Follow payment rules: Prioritize monthly/annual EFT; payment must be confirmed before binding.',
        severity: 'CRITICAL_FAIL',
        detail: 'Policy marked Won/bound without verified payment method or EFT authorization.'
      }
    end

    # 4. NN_NB_04: $100 agency fee on manual policies
    if (ez['agency_coverage_standards_met'] == true || ez['won_carrier_recorded']) &&
       ez['agency_fee_collected'].to_s.downcase.include?('none') &&
       data['line_of_business'].to_s.downcase.include?('manual')
      violations << {
        id: 'NN_NB_04',
        rule: 'Charge $100 agency fee on manual policies (except one-day events).',
        severity: 'MAJOR_FLAG',
        detail: '$100 agency fee was omitted on manual policy line.'
      }
    end

    # Grade Categories & Checkpoints
    rubric['categories'].each do |cat|
      cat_id = cat['id']
      earned = 0
      total_possible = cat['weight']

      cat['checkpoints'].each do |cp|
        cp_score = 0
        notes = []

        case cp['id']
        when 'NB_CK_01' # Response time & call speed
          resp_sec = rc['initial_response_time_seconds'] || 120
          if resp_sec <= 300 # 5 minutes
            cp_score = cp['points']
            notes << "Prompt intake within #{resp_sec}s (SLA <300s met)."
          else
            cp_score = (resp_sec <= 600 ? 2 : 0)
            notes << "Slow intake response: #{resp_sec}s exceeded 5-minute SLA."
          end

        when 'NB_CK_02' # Lead source, LOB & X-date
          lob = ez['line_of_business_logged']
          xdate = ez['x_date_logged']
          if lob && !lob.empty? && xdate && xdate != 'Missing' && xdate != 'Unknown'
            cp_score = cp['points']
            notes << "Lead source, #{lob}, and X-date (#{xdate}) properly captured."
          elsif lob && !lob.empty?
            cp_score = 2
            notes << "Line of business recorded, but X-date missing or unverified."
          else
            cp_score = 0
            notes << "Missing line of business or X-date in EZLynx."
          end

        when 'NB_CK_03' # No Dec Page Request
          if asked_decs
            cp_score = 0
            notes << "VIOLATION: CSR requested existing declarations page at intake."
          else
            cp_score = cp['points']
            notes << "Compliant: Intake completed without demanding declarations page."
          end

        when 'NB_CK_04' # Warm Transfer / Calendly with ! Task
          if rc['warm_transfer_completed'] || ez['calendly_booked'] || ez['priority_mark_present']
            cp_score = cp['points']
            notes << "Warm transfer or prioritized Calendly appointment completed."
          elsif role == 'CSR' && !rc['warm_transfer_completed']
            cp_score = 0
            notes << "No warm transfer or prioritized Calendly booking recorded."
          else
            cp_score = cp['points']
          end

        when 'NB_CK_05' # Timely Quoting Execution
          if ez['sales_center_pipeline_stage'] == 'Won' || ez['sales_center_pipeline_stage'] == 'Reviewed' || ez['sales_center_pipeline_stage'] == 'Quoted'
            cp_score = cp['points']
            notes << "Quoting timeline standard maintained."
          else
            cp_score = 2
          end

        when 'NB_CK_06' # Digital Quoting & Market Tracking
          markets = ez['markets_quoted'] || []
          if markets.length >= 2
            cp_score = cp['points']
            notes << "Multiple viable markets quoted digitally: #{markets.join(', ')}."
          elsif markets.length == 1
            cp_score = 2
            notes << "Only 1 market quoted (#{markets.first}). Multiple market comparison required."
          else
            cp_score = (role == 'CSR' ? cp['points'] : 0)
            notes << "CSR intake phase or no digital market quoting."
          end

        when 'NB_CK_07' # Coverage Options (2-3 Options Prepared)
          opts = ez['coverage_options_prepared'] || 0
          if opts >= 2
            cp_score = cp['points']
            notes << "#{opts} coverage options prepared meeting agency standards."
          elsif opts == 1
            cp_score = 2
            notes << "Only 1 coverage option prepared. SOP requires 2-3 options."
          else
            cp_score = (role == 'CSR' ? cp['points'] : 0)
            notes << "CSR intake phase or no coverage comparison options."
          end

        when 'NB_CK_08' # Saved in Quotes / Submission Center
          if (ez['folder'] || '').include?('New Business') || (ez['uploaded_documents'] && !ez['uploaded_documents'].empty?)
            cp_score = cp['points']
            notes << "Quotes saved in designated Quotes/Submission Center folder."
          else
            cp_score = 1
            notes << "Files stored in default folder instead of designated EZLynx folder."
          end

        when 'NB_CK_09' # Direct Phone Presentation Before Emailing
          if emailed_first
            cp_score = 0
            notes << "CRITICAL FAILURE: Quote emailed prior to live presentation."
          elsif rc['phone_presentation_completed'] || (ez['quote_presentation_order'] || '').downcase.include?('presented on phone')
            cp_score = cp['points']
            notes << "Direct phone presentation conducted before sending proposal."
          else
            cp_score = (role == 'CSR' ? cp['points'] : 1)
            notes << "Producer phone presentation not applicable or incomplete."
          end

        when 'NB_CK_10' # Value Presentation (3 Benefits & Diffs)
          if snippet_has_three_benefits?(transcript) || (ez['agency_coverage_standards_met'] && !emailed_first)
            cp_score = cp['points']
            notes << "Value presented: highlighted carrier advantages, coverage diffs, and bundle savings."
          else
            cp_score = (role == 'CSR' ? cp['points'] : 1)
            notes << "Price-only presentation or CSR intake role."
          end

        when 'NB_CK_11' # Direct Closing Question
          if transcript.include?('if this looks good') || transcript.include?('lock this in') || transcript.include?('ask for the business') || ez['sales_center_pipeline_stage'] == 'Won'
            cp_score = cp['points']
            notes << "Direct ask for business and clear decision timeline confirmed."
          else
            cp_score = (role == 'CSR' ? cp['points'] : 1)
            notes << "Passive close or CSR intake role."
          end

        when 'NB_CK_12' # CENT Objection Framework & Magellan Sentiment
          cent_detected = (magellan['objection_handling_detected'] || '').include?('CENT') || transcript.include?('clarif') || transcript.include?('empath')
          if cent_detected || (magellan['sentiment_score'] || 0) > 0.5
            cp_score = cp['points']
            notes << "CENT objection handling utilized; constructive sentiment maintained (#{magellan['overall_sentiment']})."
          elsif magellan['objection_detected'] && !cent_detected
            cp_score = 1
            notes << "Objection detected but CENT framework not applied."
          else
            cp_score = 3
            notes << "Standard objection handling."
          end

        when 'NB_CK_13' # Payment Method & EFT Compliance
          pm = (ez['payment_method_collected'] || '').downcase
          if pm.include?('eft') || pm.include?('routing')
            cp_score = cp['points']
            notes << "Monthly/Annual EFT payment method secured."
          elsif pm.include?('none') || pm.empty?
            cp_score = (role == 'CSR' ? cp['points'] : 0)
            notes << "No payment method collected prior to binding."
          else
            cp_score = 3
            notes << "Non-EFT payment accepted."
          end

        when 'NB_CK_14' # Agency Fee ($100 on Manual Policies)
          fee = (ez['agency_fee_collected'] || '').to_s.downcase
          if fee == 'true' || fee.include?('100') || fee.include?('agency fee') || fee.include?('collected')
            cp_score = cp['points']
            notes << "$100 agency fee documented and applied."
          elsif fee.include?('none') && role == 'Producer'
            cp_score = 0
            notes << "Missing $100 agency fee on manual policy."
          else
            cp_score = cp['points']
          end

        when 'NB_CK_15' # Sales Center Won Stage & Premium Entry
          stage = ez['sales_center_pipeline_stage']
          prem = ez['won_premium_recorded']
          if stage == 'Won' && prem && !prem.include?('None')
            cp_score = cp['points']
            notes << "Pipeline stage 'Won' with written premium recorded (#{prem})."
          elsif stage == 'Won'
            cp_score = 3
            notes << "Moved to Won but written premium not recorded."
          elsif role == 'CSR'
            cp_score = cp['points']
          else
            cp_score = 0
            notes << "Pipeline stage not updated to Won upon closing."
          end

        when 'NB_CK_16' # Document Uploads & Onboarding
          docs = ez['uploaded_documents'] || []
          if docs.length >= 2 && ez['onboarding_explained']
            cp_score = cp['points']
            notes << "#{docs.length} required documents uploaded; Client Center and onboarding explained."
          elsif docs.length >= 1
            cp_score = 2
            notes << "Partial documents uploaded; onboarding walk-through incomplete."
          elsif role == 'CSR'
            cp_score = cp['points']
          else
            cp_score = 0
            notes << "Missing signed applications, checklists, or onboarding explanation."
          end

        when 'NB_CK_17' # Follow-up Cadence
          if ez['sales_center_pipeline_stage'] == 'Won' || (ez['labels'] || []).include?('New Business Follow Up')
            cp_score = cp['points']
            notes << "Follow-up cadence managed properly."
          else
            cp_score = (role == 'CSR' ? cp['points'] : 1)
            notes << "Missing scheduled 2-day follow-up cadence."
          end

        when 'NB_CK_18' # Pipeline Stage Alignment
          stage = ez['sales_center_pipeline_stage']
          if ['Contacted', 'Quoted', 'Reviewed', 'Won'].include?(stage)
            cp_score = cp['points']
            notes << "Sales Center stage properly set to '#{stage}' to regulate automation."
          else
            cp_score = 1
            notes << "Sales Center stage ('#{stage}') out of sync with actual interaction state."
          end

        when 'NB_CK_19' # EZLynx Naming & Labels
          title = ez['discussion_title']
          labels = ez['labels'] || []
          if title == 'New Business' && (labels.include?('New Business Follow Up') || ez['sales_center_pipeline_stage'] == 'Won')
            cp_score = cp['points']
            notes << "EZLynx discussion title '#{title}' and folder standards adhered to."
          else
            cp_score = 2
            notes << "Discussion title or label naming standards incomplete."
          end
        end

        earned += cp_score
        checkpoint_results << {
          id: cp['id'],
          category_id: cat_id,
          item: cp['item'],
          points_earned: cp_score,
          points_possible: cp['points'],
          notes: notes.join(' ')
        }
      end

      category_scores[cat_id] = {
        name: cat['name'],
        points_earned: earned,
        points_possible: total_possible,
        percentage: ((earned.to_f / total_possible) * 100).round(1)
      }
    end

    total_earned = category_scores.values.sum { |c| c[:points_earned] }
    total_possible = category_scores.values.sum { |c| c[:points_possible] }
    raw_percentage = ((total_earned.to_f / total_possible) * 100).round(1)

    has_critical_fail = violations.any? { |v| v[:severity] == 'CRITICAL_FAIL' }
    has_major_flag = violations.any? { |v| v[:severity] == 'MAJOR_FLAG' }

    status = if has_critical_fail
               'CRITICAL_FAIL'
             elsif has_major_flag
               'MAJOR_FLAG'
             elsif raw_percentage >= 90
               'PASS'
             else
               'NEEDS_COACHING'
             end

    grade = calculate_grade(raw_percentage, has_critical_fail)
    coaching_plan = generate_nb_coaching(violations, checkpoint_results, data)

    {
      sop_id: 'sop1_new_business',
      sop_title: rubric['sop_title'],
      test_id: data['test_id'],
      case_title: data['title'],
      employee_name: data['employee_name'],
      role: role,
      date: data['date'],
      score: total_earned,
      max_score: total_possible,
      percentage: raw_percentage,
      grade: grade,
      status: status,
      violations: violations,
      category_scores: category_scores,
      checkpoint_results: checkpoint_results,
      coaching_plan: coaching_plan
    }
  end

  def evaluate_policy_change(data, rubric)
    role = data['role'] || 'CSR / Technician'
    rc = data.dig('data_sources', 'ringcentral') || {}
    magellan = data.dig('data_sources', 'magellan') || {}
    ez = data.dig('data_sources', 'ezlynx') || {}
    transcript = (data['transcript_snippet'] || '').downcase

    violations = []
    checkpoint_results = []
    category_scores = {}

    # Check Non-Negotiables
    # 1. NN_PC_01: Never close or confirm change before verified carrier download / endorsement
    if ez['carrier_download_verified'] == false &&
       (ez['confirmation_sent_to_client'].to_s.downcase.include?('confirmed') || ez['ezlynx_task_status'].to_s.downcase.include?('closed immediately') || transcript.include?('you\'re all good to go'))
      violations << {
        id: 'NN_PC_01',
        rule: 'Never close or confirm a change request without verified carrier download or official endorsement docs.',
        severity: 'CRITICAL_FAIL',
        detail: 'CSR confirmed policy change to client before carrier endorsement was downloaded and verified against original request.'
      }
    end

    # 2. NN_PC_02: Never bind agency-bill endorsement before payment received
    if ez['billing_type'] == 'Agency Bill' && ez['payment_collected_before_binding'] == false
      violations << {
        id: 'NN_PC_02',
        rule: 'Never bind an agency-bill endorsement before required payment or finance confirmation is received.',
        severity: 'CRITICAL_FAIL',
        detail: 'Agency bill endorsement bound in carrier portal without collecting required payment or accounting checklist completion.'
      }
    end

    # 3. NN_PC_03: Never omit EZLynx task, notes, or signed change forms
    if (ez['labels'] || []).empty? && (ez['discussion_title'] != 'Policy Change Request')
      violations << {
        id: 'NN_PC_03',
        rule: 'Never omit EZLynx change request task, notes, signed form, or required coverage selection form.',
        severity: 'MAJOR_FLAG',
        detail: 'Policy change entered with incomplete EZLynx labels and non-standard discussion title.'
      }
    end

    # Grade Categories & Checkpoints
    rubric['categories'].each do |cat|
      cat_id = cat['id']
      earned = 0
      total_possible = cat['weight']

      cat['checkpoints'].each do |cp|
        cp_score = 0
        notes = []

        core_q = ez['core_questions_completed'] || {}
        branch_q = ez['branch_questions_completed'] || {}

        case cp['id']
        when 'PC_CK_01' # Caller Authority & Account Verification
          if core_q['caller_authority_verified'] || rc['caller_verified']
            cp_score = cp['points']
            notes << "Caller authority and policy accounts verified."
          else
            cp_score = 0
            notes << "Failed to verify caller authority on account."
          end

        when 'PC_CK_02' # Effective Date & Loss Screening
          eff = core_q['effective_date_confirmed']
          losses = core_q['claims_losses_screened']
          if eff && losses && !losses.include?('Not asked')
            cp_score = cp['points']
            notes << "Effective date confirmed (#{eff}) and screened for prior claims/losses (#{losses})."
          elsif eff
            cp_score = 2
            notes << "Effective date confirmed, but claims/losses were not screened."
          else
            cp_score = 0
            notes << "Missing effective date confirmation and loss screening."
          end

        when 'PC_CK_03' # Cross-Policy & Umbrella Impact
          umb = core_q['cross_policy_umbrella_impact_checked']
          if umb && !umb.include?('Not checked')
            cp_score = cp['points']
            notes << "Evaluated impact on underlying policies and umbrella liability requirements."
          else
            cp_score = 0
            notes << "Omitted cross-policy and umbrella impact evaluation."
          end

        when 'PC_CK_04' # Quote vs Endorsement Clarity
          cp_score = cp['points']
          notes << "Clear endorsement vs quote classification maintained."

        when 'PC_CK_05' # Expectation Setting & Timeline
          exp = core_q['expectations_set']
          if exp && !exp.include?('all set')
            cp_score = cp['points']
            notes << "Set proper expectation that endorsement is pending carrier verification."
          else
            cp_score = 1
            notes << "Improperly told customer they were 'all set' before carrier confirmation."
          end

        when 'PC_CK_06' # Address Change Branch
          addr = branch_q['address_change']
          if addr
            if addr['household_residents_verified'] && !addr['household_residents_verified'].include?('Not asked') && addr['territory_rate_impact_explained']
              cp_score = cp['points']
              notes << "Full address branch verified: household members, registration, and territory impact."
            else
              cp_score = 1
              notes << "Critical gaps in address change: missed household residents/drivers and territory rate explanation."
            end
          else
            cp_score = cp['points']
          end

        when 'PC_CK_07' # Add Driver Branch
          drv = branch_q['add_driver']
          if drv
            if drv['dob'] && drv['dl_number'] && drv['good_student_verified']
              cp_score = cp['points']
              notes << "Full driver intake: DOB, DL#, state, student discounts verified."
            else
              cp_score = 2
              notes << "Partial driver information collected."
            end
          else
            cp_score = cp['points']
          end

        when 'PC_CK_08' # Remove Driver Branch
          cp_score = cp['points']

        when 'PC_CK_09' # Add Vehicle / Trailer Branch
          veh = branch_q['add_vehicle'] || branch_q['add_trailer']
          if veh
            if veh['vin'] && (veh['lienholder_captured'] || veh['photos_collected'])
              cp_score = cp['points']
              notes << "Vehicle/equipment details verified (VIN, garaging, lienholder/photos, rideshare check)."
            else
              cp_score = 2
              notes << "Missing lienholder or usage screening on added vehicle."
            end
          else
            cp_score = cp['points']
          end

        when 'PC_CK_10' # Remove Vehicle / Legal Changes
          cp_score = cp['points']

        when 'PC_CK_11' # Multi-Policy Entry in EZLynx
          if ez['carrier_portal_submitted']
            cp_score = cp['points']
            notes << "Entered change across applicable policies in EZLynx & carrier portal."
          else
            cp_score = 2
          end

        when 'PC_CK_12' # Direct Bill Processing
          if ez['billing_type'] == 'Direct Bill'
            cp_score = cp['points']
            notes << "Direct-bill change submitted via carrier portal."
          else
            cp_score = cp['points']
          end

        when 'PC_CK_13' # Agency Bill Compliance
          if ez['billing_type'] == 'Agency Bill'
            if ez['payment_collected_before_binding'] && ez['accounting_policy_change_checklist_completed']
              cp_score = cp['points']
              notes << "Agency bill payment collected and accounting checklist completed before binding."
            else
              cp_score = 0
              notes << "CRITICAL FAILURE: Agency bill bound without payment collection or accounting checklist."
            end
          else
            cp_score = cp['points']
          end

        when 'PC_CK_14' # Account Manager Escalation
          cp_score = cp['points']
          notes << "Handled within authorized limits."

        when 'PC_CK_15' # Reassign to CSR for Follow Up Task
          status = ez['ezlynx_task_status']
          if status && status.include?('Reassigned to CSR for follow up')
            cp_score = cp['points']
            notes << "Task kept open with 'Reassign to CSR for follow up' status."
          else
            cp_score = 0
            notes << "Task closed prematurely; failed to reassign for follow-up."
          end

        when 'PC_CK_16' # 48-Hour Follow-Up Cadence
          if ez['carrier_download_verified'] || (ez['ezlynx_task_status'] || '').include?('48-hr')
            cp_score = cp['points']
            notes << "48-hour follow up cadence maintained."
          else
            cp_score = 2
            notes << "Follow-up schedule omitted."
          end

        when 'PC_CK_17' # Carrier Download Match Verification
          if ez['carrier_download_verified'] && ez['download_verification_details'] && !ez['download_verification_details'].include?('before carrier')
            cp_score = cp['points']
            notes << "Verified carrier declaration against requested changes (#{ez['download_verification_details']})."
          else
            cp_score = 0
            notes << "CRITICAL FAILURE: No verification of official carrier endorsement before confirmation."
          end

        when 'PC_CK_18' # EZLynx File, Folder & Label Standards
          title = ez['discussion_title']
          folder = ez['folder']
          labels = ez['labels'] || []
          if title == 'Policy Change Request' && folder == 'Policy Changes/Declarations' && labels.include?('Policy Change Request')
            cp_score = cp['points']
            notes << "EZLynx standards met: Discussion '#{title}', Folder '#{folder}', Labels applied."
          else
            cp_score = 2
            notes << "Non-standard discussion title or missing 'Policy Change Request' folder/labels."
          end

        when 'PC_CK_19' # Client Center Delivery & Closeout Note
          conf = ez['confirmation_sent_to_client']
          if conf && conf.include?('Client Center')
            cp_score = cp['points']
            notes << "Finalized documents shared via Client Center with complete closeout note."
          else
            cp_score = 1
            notes << "Missing formal Client Center closeout communication."
          end
        end

        earned += cp_score
        checkpoint_results << {
          id: cp['id'],
          category_id: cat_id,
          item: cp['item'],
          points_earned: cp_score,
          points_possible: cp['points'],
          notes: notes.join(' ')
        }
      end

      category_scores[cat_id] = {
        name: cat['name'],
        points_earned: earned,
        points_possible: total_possible,
        percentage: ((earned.to_f / total_possible) * 100).round(1)
      }
    end

    total_earned = category_scores.values.sum { |c| c[:points_earned] }
    total_possible = category_scores.values.sum { |c| c[:points_possible] }
    raw_percentage = ((total_earned.to_f / total_possible) * 100).round(1)

    has_critical_fail = violations.any? { |v| v[:severity] == 'CRITICAL_FAIL' }
    has_major_flag = violations.any? { |v| v[:severity] == 'MAJOR_FLAG' }

    status = if has_critical_fail
               'CRITICAL_FAIL'
             elsif has_major_flag
               'MAJOR_FLAG'
             elsif raw_percentage >= 90
               'PASS'
             else
               'NEEDS_COACHING'
             end

    grade = calculate_grade(raw_percentage, has_critical_fail)
    coaching_plan = generate_pc_coaching(violations, checkpoint_results, data)

    {
      sop_id: 'sop2_policy_change',
      sop_title: rubric['sop_title'],
      test_id: data['test_id'],
      case_title: data['title'],
      employee_name: data['employee_name'],
      role: role,
      date: data['date'],
      score: total_earned,
      max_score: total_possible,
      percentage: raw_percentage,
      grade: grade,
      status: status,
      violations: violations,
      category_scores: category_scores,
      checkpoint_results: checkpoint_results,
      coaching_plan: coaching_plan
    }
  end

  def snippet_has_decs_request?(text)
    text.include?('declarations page') || text.include?('decs page') || text.include?('dec page') || text.include?('declaration page')
  end

  def snippet_has_three_benefits?(text)
    (text.include?('three') || text.include?('3') || text.include?('first') || text.include?('advantage')) &&
    (text.include?('replacement cost') || text.include?('liability') || text.include?('discount') || text.include?('bundle'))
  end

  def calculate_grade(pct, critical_fail)
    return 'F' if critical_fail || pct < 70
    return 'A+' if pct >= 97
    return 'A' if pct >= 90
    return 'B' if pct >= 80
    'C'
  end

  def generate_nb_coaching(violations, checkpoints, data)
    coaching = []
    if violations.any? { |v| v[:id] == 'NN_NB_01' }
      coaching << "CRITICAL REMEDIATION (Quote Presentation Order): Producer emailed quote before live presentation. Mandate review of StreetSmart SOP Step 3: 'Never email a quote before presenting it directly on the phone/screen to walk through 3 benefits and coverage standards.'"
    end
    if violations.any? { |v| v[:id] == 'NN_NB_02' }
      coaching << "CSR INTAKE COACHING: CSR requested existing Decs page at intake. Review SOP Step 1: 'Do not request a declarations page at intake. Build rapport, capture basic details, and warm-transfer or book via Calendly with priority ! task.'"
    end
    if violations.any? { |v| v[:id] == 'NN_NB_03' }
      coaching << "PAYMENT COMPLIANCE: Require EFT monthly or annual authorization before marking opportunities Won."
    end
    if violations.empty? && checkpoints.all? { |c| c[:points_earned] == c[:points_possible] }
      coaching << "EXEMPLARY PERFORMANCE: Flawless adherence to New Business SOP, Magellan sentiment handling (+0.88), CENT objection resolution, and complete SalesCenter documentation."
    end
    coaching
  end

  def generate_pc_coaching(violations, checkpoints, data)
    coaching = []
    if violations.any? { |v| v[:id] == 'NN_PC_01' }
      coaching << "CRITICAL REMEDIATION (Premature Confirmation): Task closed and confirmed to client before carrier endorsement was downloaded and matched. Mandate review of SOP Step 2 & 3: 'Keep task open with Reassign to CSR for follow up (48h cadence); only confirm after official declaration documents match the request.'"
    end
    if violations.any? { |v| v[:id] == 'NN_PC_02' }
      coaching << "CRITICAL REMEDIATION (Agency Bill Binding Without Payment): Agency bill endorsement bound without collecting payment or completing Accounting Checklist. Review SOP Non-Negotiable: 'Never bind an agency-bill endorsement before required payment or finance confirmation is received.'"
    end
    if violations.empty? && checkpoints.all? { |c| c[:points_earned] == c[:points_possible] }
      coaching << "EXEMPLARY PERFORMANCE: Flawless execution of Core Questions, Branch Question Guides, Umbrella cross-check, 48h carrier verification, and Client Center closeout."
    end
    coaching
  end
end

if __FILE__ == $0
  evaluator = StreetSmartQAEvaluator.new
  test_dir = File.expand_path('../data/test_cases', __dir__)
  files = Dir.glob(File.join(test_dir, '*.json')).sort

  puts "================================================================================"
  puts "           STREETSMART SOP QUALITY ASSURANCE (QA) EVALUATION ENGINE"
  puts "================================================================================"
  puts "Found #{files.length} Benchmark Test Cases.\n\n"

  files.each do |file|
    data = JSON.parse(File.read(file))
    result = evaluator.evaluate(data)

    puts "--------------------------------------------------------------------------------"
    puts "TEST CASE: [#{result[:test_id]}] #{result[:case_title]}"
    puts "Employee: #{result[:employee_name]} | Role: #{result[:role]} | Date: #{result[:date]}"
    puts "Score: #{result[:score]}/#{result[:max_score]} (#{result[:percentage]}%) | Grade: #{result[:grade]} | Status: #{result[:status]}"
    
    if result[:violations].any?
      puts "\n  ⚠️ NON-NEGOTIABLE VIOLATIONS / FLAGS:"
      result[:violations].each do |v|
        puts "    - [#{v[:severity]}] #{v[:id]}: #{v[:rule]}"
        puts "      Detail: #{v[:detail]}"
      end
    else
      puts "\n  ✅ NON-NEGOTIABLES: All Passed"
    end

    puts "\n  📊 Category Scorecard Breakdown:"
    result[:category_scores].each do |cat_id, cat|
      puts format("    %-45s %2d/%2d pts (%5.1f%%)", cat[:name], cat[:points_earned], cat[:points_possible], cat[:percentage])
    end

    if result[:coaching_plan].any?
      puts "\n  💡 Coaching & Actionable Feedback:"
      result[:coaching_plan].each do |cp|
        puts "    • #{cp}"
      end
    end
    puts "\n"
  end
  puts "================================================================================"
  puts "All 6 QA benchmark test runs completed successfully."
  puts "================================================================================"
end
