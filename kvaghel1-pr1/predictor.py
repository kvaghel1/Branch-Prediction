import sys


def local_compute(ip):
	#Local prediction
	from_addr = int(ip[0])
	ip_status = str(ip[1])
	to_addr = int(ip[2])

	global local_arr_old
	global local_arr_new
	global local_arr_pred

	local_arr_old[from_addr] = local_arr_new[from_addr]

	if local_arr_old[from_addr] == 0 or local_arr_old[from_addr] == 1:
		local_arr_pred[from_addr] = "n"
	else:
		local_arr_pred[from_addr] = "t"

	#0 1 2 3
	if ip_status == "t":
		local_arr_new[from_addr] = local_arr_old[from_addr] + 1
		local_arr_new[from_addr] = min(3,local_arr_new[from_addr]) 
	else:
		local_arr_new[from_addr] = local_arr_old[from_addr] - 1
		local_arr_new[from_addr] = max(0,local_arr_new[from_addr])

	return local_arr_pred[from_addr]

temp = "n"
start_addr = 0
def global_compute(ip):
	#Global prediction
	from_addr = int(ip[0])
	ip_status = str(ip[1])
	to_addr = int(ip[2])


	global temp
	global start_addr
	prev_status = temp
	temp = ip_status

	global global_arr_old
	global global_arr_new
	global global_arr_pred

	#Bitwise shift
	temp_addr = format(int(start_addr),"006b")
	
	temp_len = len(temp_addr)
	new_addr = [0,0,0,0,0,0]
	for i in xrange(5):
		new_addr[i] = temp_addr[i+1]

	if prev_status == "n":
		new_addr[-1] = "0"
	else:
		new_addr[-1] = "1"

	new_addr = "".join(new_addr)
	tn = new_addr
	new_addr = int(new_addr,2)
	start_addr = new_addr

	global_arr_old[new_addr] = global_arr_new[new_addr]

	if global_arr_old[new_addr] == 0 or global_arr_old[new_addr] == 1:
		global_arr_pred[new_addr] = "n"
	else:
		global_arr_pred[new_addr] = "t"

	#0 1 2 3 
	if ip_status == "t":
		global_arr_new[new_addr] = global_arr_old[new_addr] + 1
		global_arr_new[new_addr] = min(3,global_arr_new[new_addr]) 
	else:
		global_arr_new[new_addr] = global_arr_old[new_addr] - 1 
		global_arr_new[new_addr] = max(0,global_arr_new[new_addr])

	return global_arr_pred[new_addr]

def selector_compute(global_pred,local_pred,ip):
	#Tournament prediction
	from_addr = int(ip[0])
	ip_status = str(ip[1])
	to_addr = int(ip[2])
	actual_pred = ip_status


	final_pred = ""

	global selector_arr_old
	global selector_arr_new
	global selector_arr_pred


	selector_arr_old[from_addr] = selector_arr_new[from_addr]

	#Current prediction
	if selector_arr_old[from_addr] == 0 or selector_arr_old[from_addr] == 1:
		selector_arr_pred[from_addr] = "L"
	else:
		selector_arr_pred[from_addr] = "G"

	#Make Prediction
	if local_pred == global_pred:
		#no update
		selector_arr_new[from_addr] = selector_arr_old[from_addr]
	else:
		if local_pred == actual_pred:
			#decrement
			selector_arr_new[from_addr] = selector_arr_old[from_addr] - 1
			selector_arr_new[from_addr] = max(0,selector_arr_new[from_addr])
		else:
			selector_arr_new[from_addr] = selector_arr_old[from_addr] + 1
			selector_arr_new[from_addr] = min(3,selector_arr_new[from_addr])

	#Final prediction
	if selector_arr_pred[from_addr] == "L":
		#choose local
		final_pred = local_pred
	else:
		final_pred = global_pred

	final_output = str(from_addr) + str(local_pred) + str(global_pred) + str(selector_arr_pred[from_addr]).lower() + str(final_pred) + str(actual_pred)
	#print final_output

	return final_output

def main(input_file):
	
	global local_arr_old
	global local_arr_new
	global local_arr_pred

	global global_arr_old
	global global_arr_new
	global global_arr_pred

	global selector_arr_old
	global selector_arr_new
	global selector_arr_pred


	local_arr_old = [0]*10 #[0,0,0,0,0,0,0,0,0]
	local_arr_new = [0]*10
	local_arr_pred = [""]*10
	
	global_arr_old = [0]*64 #[0,0,0,0,0,0,0,0,0]
	global_arr_new = [0]*64
	global_arr_pred = [""]*64
	
	selector_arr_old = [0]*10 #[0,0,0,0,0,0,0,0,0]
	selector_arr_new = [0]*10
	selector_arr_pred = [""]*10
	for line in sys.stdin:
	 	ip = line.strip("\n")
		if len(ip) > 0:
			local_pred = local_compute(ip)
			global_pred = global_compute(ip)
			c = selector_compute(global_pred,local_pred,ip)
			print c

if __name__ == '__main__':
	print (sys.stdin)
	#main(sys.stdin)