=================
gsm-modem-asyncio
=================

Async GSM modem control library

Overview
========

This library allows to control GSM modem connected over serial interface asynchronously. Current features are listed below.

Features
========

 * Check CSQ
 * Send USSD
 * Send SMS
 * Make call

Usage
=====

.. code-block:: python

    gsm_modem = GsmModem('/dev/ttyS0')
    print('CSQ:', await gsm_modem.get_csq())
    print('USSD reply:', await gsm_modem.send_ussd('*111#'))
    await gsm_modem.send_sms(number='123456789', text='Hello!')
    await gsm_modem.call(number='123456789', seconds=60)

Install
=======

Install package:

.. code-block:: bash

    python3 setup.py install

Run tests (optionally):

.. code-block:: bash

    python3 -m unittest discover tests
