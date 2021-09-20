-- example HTTP POST script which demonstrates setting the
-- HTTP method, body, and adding a header
--
local math = require "math"

local paras = {}
table.insert(paras,'123')
table.insert(paras,'456')

-- math.randomseed(tonumber(tostring(os.time()):reverse():sub(1,6)))
-- math.randomseed(tonumber(tostring(os.time())))


function rdm_f()
    rdm = math.random()
--     if(rdm > 0.5) then
--        para = paras[1]
--     else
--        para = paras[2]
--     end
    return rdm
end

counter = 0
num = 0
request = function()
   path = "/?arg=" .. rdm_f()
   return wrk.format("GET", path)
end