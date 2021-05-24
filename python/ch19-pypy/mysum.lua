local starttime = os.clock();
local number = 0
local total = 100000000-1
for i=total,1,-1 do
    number = number+i
end
print(number)
local endtime = os.clock();
print(string.format("elapsed time  : %.4f", endtime - starttime));