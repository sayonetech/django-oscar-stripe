Django-Oscar-Stripe
=====================

********
Features
********

* Make a simple stripe transaction.
* Store details of the transaction in Database Backend.
* Page for listing the transactions.
* Page showing the details of a Transaction.


**********
How to Use
**********

* Download the project from git.
* Copy the oscar_stripe folder into your project.
* Add 'oscar_stripe' into your 'installed_apps'
* Run migrate command.
* Include the urls mentioned in the dashboard into the projects root urls.

*************
Example Usage
*************

* Make transaction

    from oscar_stripe import simple_payment

    response = simple_payment('123456789', 12.50, 'usd', bank_card_object)


*************
Parameters
*************

==================  ================ ===================   =====================================================
Parameter Name        Required        Type(max length)                       Description
==================  ================ ===================   =====================================================
order_number          Yes             varchar                    Order number to show in description.
amount                Yes             decimal                    Amount to be transferred in decimal.
currency              Yes             varchar(3)                 Currency for stripe transaction.
bankcard              Yes             Object                     Bankcard object using which payment is done.
Billing_address       No              dictionary                 Billing address with fields first_name, last_name,
                                                                 street, city, state, zip.
description           No              varchar                    description to be mentioned in transaction(
                                                                 default:order_number).
==================  ================ ===================   =====================================================
