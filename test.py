
samples_dict = {}
sample_spacing = 30

for i in range(1, 37):
    x = (i - 1) % 6
    y = (i - 1) // 6
    samples_dict[i] = [x, y]

cord_dict = {}
for sample in range(1,37):
    x = 30 + (samples_dict[sample][0] * sample_spacing)
    y = 30 + (samples_dict[sample][1] * sample_spacing)
    cord_dict[sample] = [x,y]

samples_list = [1,2,3,36,27]
for sample in samples_list:
    print (f"Sample {sample} on {cord_dict[sample]}")