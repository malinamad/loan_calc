import math
import argparse


def interest_rate_formula(loan_interest):
    return loan_interest / (12 * 100)


def monthly_payment_formula(loan_principal,
                            periods,
                            loan_interest):
    nominal_interest_rate = interest_rate_formula(loan_interest)
    ordinary_annuity = loan_principal * ((nominal_interest_rate * math.pow(1 + nominal_interest_rate, periods))
                                         / (math.pow(1 + nominal_interest_rate, periods) - 1))
    return math.ceil(ordinary_annuity)


def loan_principal_formula(annuity_payment,
                           pay_num,
                           loan_interest):
    nominal_interest_rate = interest_rate_formula(loan_interest)
    principal = annuity_payment \
                / ((nominal_interest_rate * (math.pow(1 + nominal_interest_rate, pay_num)))
                   / ((math.pow(1 + nominal_interest_rate, pay_num)) - 1))
    return principal


def the_number_of_payments_formula(loan_principal,
                                   annuity_payment,
                                   loan_interest):
    nominal_interest_rate = interest_rate_formula(loan_interest)
    first_part_result = annuity_payment / (annuity_payment - nominal_interest_rate * loan_principal)
    months_num = math.ceil(math.log(first_part_result, 1 + nominal_interest_rate))

    return months_num


def differentiated_payment(loan_principal,
                           periods,
                           loan_interest):
    m = 0
    total_diff_value = 0
    while m < periods:
        m += 1
        nominal_interest_rate = interest_rate_formula(loan_interest)
        diff_value = math.ceil((loan_principal / periods) + nominal_interest_rate * \
                               (loan_principal - (loan_principal * (m - 1) / periods)))
        total_diff_value += diff_value
        print(f'Month {m}: payment is {diff_value}')

    overpayment = round(total_diff_value - loan_principal)
    print(f'\nOverpayment = {overpayment}')


def negative_values_validation(*args):
    try:
        items_collection = {*args}
        negative_items = sum(n < 0 for n in items_collection)
        if negative_items > 0:
            return 'Incorrect parameters'
    except TypeError:
        return 'Incorrect parameters'


def print_time_to_repay(months):
    if months > 12:
        num_of_years = months // 12
        months_left = months - (num_of_years * 12)
        if num_of_years == 1 and months_left == 1:
            return f'It will take {num_of_years} year and {months_left} month to repay this loan!'
        elif num_of_years == 1:
            return f'It will take {num_of_years} year and {months_left} months to repay this loan!'
        elif months_left == 1:
            return f'It will take {num_of_years} years and {months_left} month to repay this loan!'
        elif num_of_years > 1 and months_left > 1:
            return f'It will take {num_of_years} years and {months_left} months to repay this loan!'
        elif num_of_years > 1:
            return f'It will take {num_of_years} years to repay this loan!'
        else:
            return f'It will take {num_of_years} years and {months_left} months to repay this loan!'
    elif months < 12:
        return f'It will take {months} months to repay this loan!'
    else:
        return f'It will take a year to repay this loan!'


parser = argparse.ArgumentParser(description='This program is made to compute differentiated payments.')

parser.add_argument('--type',
                    choices=['annuity', 'diff'],
                    help='You need to choose only one option from the list')
parser.add_argument('--principal', type=float)
parser.add_argument('--payment', type=float)
parser.add_argument('--periods', type=float)
parser.add_argument('--interest', type=float)

args = parser.parse_args()

payment_type = args.type
principal = args.principal
periods = args.periods
interest = args.interest
payment = args.payment

all_items = [payment_type, principal, periods,
             interest, payment]
given_args_total = sum(x is not None for x in all_items)

items_repay_args = [principal, payment, interest]
items_annuity_args = [principal, periods, interest]
items_principal_args = [payment, periods, interest]

given_args_repay = sum(x is not None for x in items_repay_args)
given_args_annuity = sum(x is not None for x in items_annuity_args)
given_args_principal = sum(x is not None for x in items_principal_args)

if given_args_total == 4:
    if payment_type == 'diff':
        if negative_values_validation(principal, periods, interest) != 'Incorrect parameters':
            differentiated_payment(principal, periods, interest)
        else:
            print('Incorrect parameters')
    elif payment_type == 'annuity':
        if given_args_principal == 3:
            if negative_values_validation(payment, periods, interest) != 'Incorrect parameters':
                loan_principal = loan_principal_formula(payment, periods, interest)
                print(f'Your loan principal = {round(loan_principal)}!')
                print(f'Overpayment {round(payment * periods - loan_principal)}')
            else:
                print('Incorrect parameters')

        elif given_args_annuity == 3:
            if negative_values_validation(principal, periods, interest) != 'Incorrect parameters':
                annuity_pay = monthly_payment_formula(principal, periods, interest)
                print(f'Your annuity payment = {annuity_pay}!')
                print(f'Overpayment {annuity_pay * periods - principal}')
            else:
                print('Incorrect parameters')

        elif given_args_repay == 3:
            if negative_values_validation(principal, payment, interest) != 'Incorrect parameters':
                num_of_months = the_number_of_payments_formula(principal, payment, interest)
                print(print_time_to_repay(num_of_months))
                print(f'Overpayment = {round(num_of_months * payment - principal)}')
            else:
                print('Incorrect parameters')
        else:
            print('Incorrect parameters')
    else:
        print('Incorrect parameters')
else:
    print('Incorrect parameters')
