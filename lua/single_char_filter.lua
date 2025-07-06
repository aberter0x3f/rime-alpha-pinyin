local function single_char_filter(input, env)
  local single_char_mode_enabled = env.engine.context:get_option("single_char_mode")

  if not single_char_mode_enabled then
    for cand in input:iter() do
      yield(cand)
    end
    return
  end

  for cand in input:iter() do
    if utf8.len(cand.text) == 1 then
      yield(cand)
    end
  end
end

return single_char_filter
