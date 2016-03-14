#loan calculator
import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

def monthly_payments(prin, intr, term, dpmt):
	irate = intr/12.0/100.0
	months = term*12
	pmt = ((prin - dpmt)*irate*(1+irate)**months)/((1+irate)**months-1)
	#print('pmt $%.2f' %pmt)
	return pmt

def calculate_payment_allocation(prin, intr, term, pmt, add, extra, dpmt, pmi):
	for i in xrange(2):
		working_add = add
		twenty_percent = prin*.8
		working_prin = prin - dpmt
		months = term*12
		irate = intr/12.0/100.0
		pmi_flag = intr_paid = prin_paid = add_paid = tot_paid = month = 0
		prin_graph = []
		intr_graph = []
		add_graph = []
		tot_graph = []
		#for month in range(0,months):
		while working_prin >= 0:
			intr_pmt = working_prin*irate
			intr_paid = intr_paid + intr_pmt
			intr_graph.append(intr_paid)
			
			prin_pmt = pmt - intr_pmt
			if i == 0:
				working_prin = working_prin - prin_pmt
				prin_paid = prin_paid + prin_pmt
				tot_paid = tot_paid + prin_pmt + intr_pmt + add
			elif i == 1:
				working_prin = working_prin - prin_pmt - extra
				prin_paid = prin_paid + prin_pmt + extra
				tot_paid = tot_paid + prin_pmt + intr_pmt + add + extra
			prin_graph.append(prin_paid)
			tot_graph.append(tot_paid)

			add_paid = add_paid + add
			add_graph.append(add_paid)
			if (working_prin <= twenty_percent) & (pmi_flag == 0):
				print("Years until PMI goes away: %.1f" % (month/12.0))
				print("Months until PMI goes away: %d" % month)
				print("PMI paid: $%.2f" % (month*pmi))
				working_add -= pmi
				pmi_flag = 1
				print('Total interest before PMI goes away: $%.2f' % intr_paid)
			month += 1

		#else:
			#print(prin)
			#if prin <= 0:
			#	print('You\'re done early! Celebrate!')
			#	break
		if 1 == False:
			print('Years to payoff: %.1f' % (month/12.0))
			print('Monthly Payments w/o PMI: $%.2f' % (pmt+extra+add))
			print('Monthly Payments w/PMI: $%.2f' % (pmt+extra+add+pmi))
			print('Monthly PMI Payments: $%.2f' % pmi)
			print('Total Interest Paid: $%.2f' % intr_paid)
			print('Total Principle Paid: $%.2f' % prin_paid)
			print('Total Principle and Interest Paid: $%.2f' % (intr_paid+prin_paid))
			print('Total Additional Expenses: $%.2f' % add_paid)
			print('Total Paid: $%.2f' % tot_paid)
		
		x = np.arange(0,month)
		if i == 0:
			fig = plt.figure(figsize=(20,10))
			ax = plt.subplot(2,2,1)
			plt.title('Standard Payment Plan')
			tot1 = tot_paid
			month1 = month
		elif i == 1:
			ax = plt.subplot(2,2,2)
			plt.title('Accelerated Payment Plan: $%d extra/month' % extra)
			tot2 = tot_paid
			month2 = month
		ax.plot(x,intr_graph,'r',x,tot_graph,'b',x,add_graph,'y',x,prin_graph,'g')
		xloc = 5
		yadj = tot_paid/20
		yloc = tot_paid - yadj
		ax.text(xloc, yloc, 'Years to payoff: %.1f' % (month/12.0))
		yloc -= yadj	
		ax.text(xloc, yloc, 'Monthly Payments w/o PMI: $%.2f' % (pmt+extra+add))
		yloc -= yadj
		ax.text(xloc, yloc, 'Monthly Payments w/PMI: $%.2f' % (pmt+extra+add+pmi))
		yloc -= yadj
		ax.text(xloc, yloc, 'Monthly PMI Payments: $%.2f' % pmi)
		yloc -= yadj
		ax.text(xloc, yloc, 'Total Interest Paid: $%.2f' % intr_paid)
		yloc -= yadj
		ax.text(xloc, yloc, 'Total Principle Paid: $%.2f' % prin_paid)
		yloc -= yadj
		ax.text(xloc, yloc, 'Total Principle and Interest Paid: $%.2f' % (intr_paid+prin_paid))
		yloc -= yadj
		ax.text(xloc, yloc, 'Total Additional Expenses: $%.2f' % add_paid)
		yloc -= yadj
		ax.text(xloc, yloc, 'Total Paid: $%.2f' % tot_paid)
		if i == 1:
			yloc -= yadj
			m_saved = tot1-tot2
			ax.text(xloc, yloc, 'Money saved: $%.2f' % m_saved)
			yloc -= yadj
			t_saved = month1-month2
			ax.text(xloc, yloc, 'Time saved: %.1f years' % (t_saved/12))
		formatter = ticker.FormatStrFormatter('$%d')
		ax.yaxis.set_major_formatter(formatter)
		plt.xlabel('Months')
		plt.ylabel('Dollars')
		
	p = m_saved
	t = t_saved/12
	n = 12
	r = .07
	A = 0
	inv_graph = np.empty(t_saved)
	for j in xrange(t_saved):
		A = A*(1 + r/n) + extra
		inv_graph[j] = A
	ax = plt.subplot(2,2,3)
	plt.plot(np.arange(t_saved), inv_graph)
	ax.text(5, A - A/20, "If we invested, we'd make $%dk in the %d extra years we'd pay the mortgage" % (A/1000, t))
	ax.text(5, (A - A/10), "This is assuming a %d pcnt interest rate" % (r*100))
	ax.text(5, (A - A*3/20), "We'd have to pay $%dk in interest and fees during that time" % (m_saved/1000))
	plt.show()

def calc_percentages(prin, dp_pcnt, tax_pcnt, ins_pcnt, hoa_q):
	dpmt = prin*dp_pcnt/100.0
	tax = prin*tax_pcnt/12.0/100.0
	if dp_pcnt < 10:
		pmi_pcnt = .78
	elif dp_pcnt < 20:
		pmi_pcnt = .52
	pmi = prin*pmi_pcnt/100.0/12
	ins = prin*ins_pcnt/100.0/12
	hoa = hoa_q/4.0
	
	if 1 == False:
		print('dpmt $%.2f' % dpmt)
		print('tax $%.2f' % tax)
		print('pmi $%.2f' % pmi)
		print('ins $%.2f' % ins)
		print('hoa $%.2f' %hoa)
		
	add = tax + pmi + ins + hoa
	return add, dpmt, pmi

principle = 210600
interest_rate = 4.0
years = 30
down_payment_fraction = 10
hoa = 57
ins_pcnt = 0.36
tax_pcnt =  1.5
extra = 1500
add, dpmt, pmi = calc_percentages(principle, down_payment_fraction, tax_pcnt, ins_pcnt, hoa)
p_month = monthly_payments(principle,interest_rate,years,dpmt)
calculate_payment_allocation(principle,interest_rate,years,p_month,add,extra,dpmt,pmi)


