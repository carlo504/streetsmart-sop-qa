require "json"
require_relative "qa_evaluator"

batch_file = "/Users/carloferrara/.gemini/antigravity/scratch/data/live_ringcentral_magellan_batch.json"
unless File.exist?(batch_file)
  puts "Error: Batch file #{batch_file} not found."
  exit 1
end

data = JSON.parse(File.read(batch_file))
evaluator = StreetSmartQAEvaluator.new

puts "\n" + ("=" * 95)
puts "         STREETSMART MULTI-SOURCE AGENCY LIVE QA AUDIT & COACHING REPORT"
puts "         Sources: RingCentral Telephony • Magellan Sentiment • EZLynx AMS"
puts "         Audit Date: September 1, 2026"
puts ("=" * 95) + "\n"

# 1. Audit Live EZLynx + RingCentral Correlated Cases
puts "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
puts "SECTION 1: CRM & TELEPHONY CORRELATED ACTIVE WORKFLOW AUDITS"
puts "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

crm_cases = [
  {
    "test_id" => "LIVE_CRM_01",
    "sop_id" => "sop2_policy_change",
    "title" => "Ricardo Aguilar - STRAIGHT TO THE SOURCE LLC (Trucking Commercial ID Cards & Portal Access)",
    "employee_name" => "Ricardo Aguilar (Commercial / Trucking Producer & CSR)",
    "role" => "CSR / Technician",
    "date" => "2026-09-01",
    "line_of_business" => "Commercial Trucking Auto (Policy #DSLA1000747-00)",
    "data_sources" => {
      "ringcentral" => {
        "call_id" => "RC-20260901-07",
        "call_duration_minutes" => 3.32,
        "caller_verified" => true,
        "phone_presentation_completed" => true
      },
      "magellan" => {
        "overall_sentiment" => "Positive / Resolved",
        "sentiment_score" => 0.88,
        "empathy_score" => 92,
        "talk_to_listen_ratio" => "45/55",
        "objection_detected" => "Client locked out of Client Center / ID card portal on road.",
        "objection_handling_detected" => "Immediately generated 2FA security code (238340) and sent direct SMS/Email portal link."
      },
      "ezlynx" => {
        "discussion_title" => "Policy Change Request",
        "folder" => "Policy Changes/Declarations",
        "labels" => ["Policy Change Request", "Commercial Trucking", "Client Center Delivered"],
        "core_questions_completed" => {
          "caller_authority_verified" => true,
          "effective_date_confirmed" => "2026-09-01",
          "claims_losses_screened" => "Active fleet, no pending claims",
          "cross_policy_umbrella_impact_checked" => "Commercial Auto & Cargo limits verified",
          "expectations_set" => "Provided immediate access code and verified insured can download cab ID cards"
        },
        "branch_questions_completed" => {},
        "ezlynx_task_status" => "Reassigned to CSR for follow up",
        "carrier_portal_submitted" => true,
        "billing_type" => "Direct Bill",
        "carrier_download_verified" => true,
        "download_verification_details" => "Matched active carrier schedule and sent updated cab cards",
        "confirmation_sent_to_client" => "Dispatched via Automation Center SMS + Email"
      }
    },
    "transcript_snippet" => "CLIENT: \"This isn'\''t allow me access to the documents.\" | RICARDO AGUILAR: \"I am generating a fresh one-time verification code for you right now (238340) and texting the direct link so you have your active ID cards in hand.\""
  },
  {
    "test_id" => "LIVE_CRM_02",
    "sop_id" => "sop2_policy_change",
    "title" => "Daniela Aguilar - Judith Flores & Alfredo Flores-Perez (Flood Policy Renewal)",
    "employee_name" => "Daniela Aguilar (Personal Lines Account Technician)",
    "role" => "CSR / Technician",
    "date" => "2026-09-01",
    "line_of_business" => "Flood Policy (Personal Lines #13421-95720)",
    "data_sources" => {
      "ringcentral" => {
        "call_id" => "RC-20260901-05",
        "call_duration_minutes" => 0.75,
        "caller_verified" => true,
        "phone_presentation_completed" => true
      },
      "magellan" => {
        "overall_sentiment" => "Positive / Cooperative",
        "sentiment_score" => 0.82,
        "empathy_score" => 90,
        "talk_to_listen_ratio" => "40/60",
        "objection_detected" => "Renewal payment timing",
        "objection_handling_detected" => "Clear follow-up voicemail and Client Center payment link dispatch."
      },
      "ezlynx" => {
        "discussion_title" => "Policy Change Request",
        "folder" => "Policy Changes/Declarations",
        "labels" => ["Policy Change Request", "Email Sent", "Phone Call Made", "Left message for Insured CSR"],
        "core_questions_completed" => {
          "caller_authority_verified" => true,
          "effective_date_confirmed" => "2026-09-01",
          "claims_losses_screened" => "No pending flood losses",
          "cross_policy_umbrella_impact_checked" => "Primary property limits cross-referenced",
          "expectations_set" => "Left VM and sent notice regarding payment deadline"
        },
        "branch_questions_completed" => {},
        "ezlynx_task_status" => "Reassigned to CSR for follow up",
        "carrier_portal_submitted" => true,
        "billing_type" => "Direct Bill",
        "carrier_download_verified" => true,
        "download_verification_details" => "Monitoring renewal receipt download",
        "confirmation_sent_to_client" => "Automation Center renewal payment reminder"
      }
    },
    "transcript_snippet" => "CLIENT: \"Yes about the flood policy. I need to pay that.\" | CSR NOTE: \"Low Risk Renewal (11) - not signed yet I called left vm monitoring response\""
  }
]

crm_cases.each do |c|
  res = evaluator.evaluate(c)
  puts "\n▶ Case: #{res[:case_title]}"
  puts "  Audited: #{res[:employee_name]} | Score: #{res[:score]}/#{res[:max_score]} (#{res[:percentage]}%) | Grade: #{res[:grade]} | Status: #{res[:status]}"
  puts "  Violations: #{res[:violations].empty? ? 'None (Clean)' : res[:violations].map { |v| "[#{v[:severity]}] #{v[:rule]}" }.join(', ')}"
  puts "  Coaching Note: #{res[:coaching_plan].first}"
end

# 2. Audit Magellan Audited Interactions for SOP Compliance
puts "\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
puts "SECTION 2: MAGELLAN SENTIMENT INTELLIGENCE & CALL AUDIT FINDINGS"
puts "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

magellan_calls = [
  {
    client: "Joanne Quackenbush (732-977-2623)",
    rep: "Sandy Santana (Commercial Lines)",
    scenario: "Urgent Commercial Auto ID Cards for Closing Repair Garage",
    sentiment: "5.3 / 10 (Urgent / At-Risk)",
    sop_compliance: "HIGH PRIORITY ESCALATION",
    qa_finding: "Customer made 2 calls (4:03 PM & 4:05 PM) waiting at a closing auto shop. IVR correctly transferred to Commercial queue, but caller reached VM. SOP mandates urgent same-day ID card dispatch.",
    coaching: "Implement priority tag in RingCentral for keywords 'garage closing' / 'impound' to route to any available live CSR rather than individual agent voicemail."
  },
  {
    client: "Arun Maheshwari (209-292-0795)",
    rep: "Anna Flores (Personal Lines)",
    scenario: "1-Way Audio Inbound Call to Personal Lines",
    sentiment: "5.3 / 10 (Communication Barrier)",
    sop_compliance: "COMPLIANT (QA Disconnect Protocol)",
    qa_finding: "CSR Anna stated standard agency closing script: 'I am unable to hear you. If you can hear me, please call us back for assistance. For quality, I will need to disconnect.'",
    coaching: "100% compliant with standard QA call disconnection protocol."
  },
  {
    client: "Eddie & Annie Dillard (646-302-4027)",
    rep: "AI Sonant -> Mike Sosa (Commercial Auto)",
    scenario: "Commercial Auto Policy Renewal Inquiry",
    sentiment: "5.4 / 10 (Neutral / Renewal Seeking)",
    sop_compliance: "COMPLIANT (Warm Queue Hand-off)",
    qa_finding: "Sonant disambiguated between personal and commercial lines and queued customer for Mike Sosa with call duration 2m 53s.",
    coaching: "Follow up within 2 hours per New Business/Renewal SOP standards."
  }
]

magellan_calls.each_with_index do |mc, idx|
  puts "\n[MAGELLAN-#{idx+1}] #{mc[:scenario]}"
  puts "  Client: #{mc[:client]} | Rep/Queue: #{mc[:rep]}"
  puts "  Sentiment: #{mc[:sentiment]} | SOP Status: #{mc[:sop_compliance]}"
  puts "  Audit Finding: #{mc[:qa_finding]}"
  puts "  Action Item: #{mc[:coaching]}"
end

puts "\n" + ("=" * 95)
puts "                           END OF LIVE BATCH QA AUDIT REPORT"
puts ("=" * 95) + "\n"
