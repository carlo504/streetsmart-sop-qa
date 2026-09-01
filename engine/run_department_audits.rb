require 'json'
require_relative 'qa_evaluator'

test_cases_file = File.join(__dir__, '../data/department_test_cases.json')
cases = JSON.parse(File.read(test_cases_file))
evaluator = StreetSmartQAEvaluator.new

departments = cases.group_by { |c| c['department'] }

puts "=" * 115
puts "      STREETSMART SOP QA AUDIT SUITE — DEPARTMENT BENCHMARK EVALUATIONS WITH CLIENT NAMES (9 CASES)"
puts "      Departments: Personal Lines • Commercial Lines • Trucking and Transportation"
puts "=" * 115
puts ""

summary_table = []

departments.each do |dept, dept_cases|
  puts "#" * 115
  puts "DEPARTMENT: #{dept.upcase} (#{dept_cases.length} Scenarios)"
  puts "#" * 115
  puts ""

  dept_cases.each_with_index do |tc, idx|
    result = evaluator.evaluate(tc)
    
    status_icon = result[:status] == 'PASS' ? '✅ PASS' : (result[:status] == 'MAJOR_FLAG' ? '⚠️ MAJOR_FLAG' : '❌ CRITICAL FAIL')
    
    summary_table << {
      dept: dept,
      test_id: tc['test_id'],
      client_name: tc['insured_name'] || tc['client_name'] || 'Unknown Client',
      account_num: tc['account_number'] || 'N/A',
      carrier_name: tc['primary_carrier'] || tc['carrier_name'] || 'Standard Carrier',
      employee: tc['employee_name'],
      role: tc['role'],
      score: "#{result[:score]}/#{result[:max_score]}",
      grade: result[:grade],
      status: result[:status]
    }

    puts "-" * 115
    puts "Scenario #{idx + 1}: #{tc['title']}"
    puts "-" * 115
    puts "👤 Client / Insured: #{tc['insured_name']} (Account: ##{tc['account_number']})"
    puts "🏢 Carrier:          #{tc['carrier_name'] || tc['primary_carrier']}"
    puts "👨‍💼 Audited Rep:      #{tc['employee_name']} (#{tc['role']})"
    puts "📄 SOP Reference:    #{tc['sop_title']} | LOB: #{tc['line_of_business']}"
    puts "📊 Audit Score:      #{result[:score]}/#{result[:max_score]} (#{(result[:score].to_f / result[:max_score] * 100).round(1)}%) | Grade: #{result[:grade]} | Status: #{status_icon}"
    puts ""

    if result[:violations].empty?
      puts "🛡️ Non-Negotiables: All Passed"
    else
      puts "🚨 Non-Negotiable Flags / Violations:"
      result[:violations].each do |v|
        puts "  • [#{v[:severity]}] #{v[:id]}: #{v[:rule]}"
        puts "    Detail: #{v[:detail]}"
      end
    end
    puts ""

    puts "📊 Category Score Breakdown:"
    result[:category_scores].each do |cat_id, cat|
      earned = cat[:points_earned] || cat[:earned] || 0
      total = cat[:points_possible] || cat[:total] || 1
      pct = (earned.to_f / total * 100).round(1)
      printf("  - %-48s %2d/%2d pts (%5.1f%%)\n", cat[:name], earned, total, pct)
    end
    puts ""

    coaching = result[:coaching_plan] || result[:actionable_feedback] || []
    if coaching.any?
      puts "💡 Actionable Coaching & Remediation Plan:"
      coaching.each do |fb|
        puts "  • #{fb}"
      end
      puts ""
    end
  end
end

puts "=" * 115
puts "                               DEPARTMENT AUDIT SUMMARY MATRIX"
puts "=" * 115
printf("%-18s | %-10s | %-32s | %-20s | %-8s | %-6s | %-13s\n", "Department", "Test ID", "Client / Insured Name", "Audited Employee", "Score", "Grade", "Status")
puts "-" * 115
summary_table.each do |row|
  printf("%-18s | %-10s | %-32s | %-20s | %-8s | %-6s | %-13s\n",
    row[:dept],
    row[:test_id],
    row[:client_name].length > 32 ? row[:client_name][0..29] + "..." : row[:client_name],
    row[:employee].length > 20 ? row[:employee][0..17] + "..." : row[:employee],
    row[:score],
    row[:grade],
    row[:status]
  )
end
puts "=" * 115
