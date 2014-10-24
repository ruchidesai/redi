import smtplib
from smtplib import SMTPException
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email import Encoders
from datetime import date
import logging

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

"""
This module groups together related functions for
sending emails.

Module unit test: test/TestRediEmail.py
"""

def send_email_redcap_connection_error(email_settings, subject='', msg=''):
    """
    Return True if the email was sent.
    Notify the designated `REDCap support` person about problems
    with reaching REDCap

    Parameters
    ----------
    email_settings : dict
        The dictionary with smtp server parameters
    subject : str
        The email subject
    msg : str
        The content to be emailed
    """

    sender = email_settings['redcap_support_sender_email']
    to_addr_list = email_settings['redcap_support_receiving_list']
    host = email_settings['smtp_host_for_outbound_mail']
    port = email_settings['smtp_port_for_outbound_mail']
    subject = 'Communication failure: Unable to reach REDCap instance'
    msg = 'A problem was encountered when connecting to the REDCap. Please investigate if REDCap is running.'

    logger.error('Exception: Unable to communicate with REDCap instance at: ' + email_settings['redcap_uri'])
    return send_email(host, str(port), sender, to_addr_list, None, subject, msg)

def send_email_input_data_unchanged(email_settings, raw_xml):
    """
    Send a warning email to the `redcap_support_receiver_email`
    if the input file did not change for more than `batch_warning_days`
    Return True if the email was sent

    Parameters
    ----------
    email_settings : dictionary
        The email delivery parameters
    raw_xml : RawXml instance
        The object storing details about the input file
    """
    sender = email_settings['redcap_support_sender_email']
    to_addr_list = email_settings['redcap_support_receiving_list']
    host = email_settings['smtp_host_for_outbound_mail']
    port = email_settings['smtp_port_for_outbound_mail']
    subject = "The data for '{0}' project did not change in more than {1} days.".format(raw_xml.get_project(), email_settings['batch_warning_days'])
    msg = """
Administrators,
    """ +  subject + """

Please check if the input xml file is in the proper location.
    """ + raw_xml.get_info()
    return send_email(host, str(port), sender, to_addr_list, None, subject, msg)


def add_attachment(msg, body):
    """
    Add the html report as attachment

    Parameters
    ----------
    msg : MIMEMultipart
        The object to which we attach the body content
    body : string
        The html content to be attached
    """
    part = MIMEBase('application', "octet-stream")
    part.set_payload(body)
    Encoders.encode_base64(part)
    file_name = "redi_report_{}.html".format(date.today())
    part.add_header('Content-Disposition', \
            'attachment; filename="{}"'.format(file_name))
    msg.attach(part)


def send_email_data_import_completed(email_settings, body=''):
    """
    Email the html report after redi completed the data transfer
    Returns a dictionary, with one entry for each recipient that was refused

    Parameters
    ----------
    email_settings : dict
        Email params produced by redi.get_email_settings()
    body : string
        The html content produced by transforming the xsl
        generated by redi.create_summary_report()
    """
    sender = email_settings['batch_report_sender_email']
    to_addr_list = email_settings['batch_report_receiving_list']
    host = email_settings['smtp_host_for_outbound_mail']
    port = email_settings['smtp_port_for_outbound_mail']
    subject = 'Data Import Report'
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = ",".join(to_addr_list)
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'html'))
    add_attachment(msg, body)

    refused_list = {}
    smtp_obj = smtplib.SMTP(host, port)
    refused_list = smtp_obj.sendmail(sender, to_addr_list, msg.as_string())
    logger.info("Successfully sent email to: " + str(to_addr_list))
    smtp_obj.quit()
    return refused_list

def send_email(
        host,
        port,
        sender,
        to_addr_list,
        cc_addr_list,
        subject,
        msg_body):
    """
    The email deliverer. Return True if the email was sent

    Parameters
    ----------
    to_addr_list : list
        The recipients of the email
    """
    #print ('host %s, port: %s' % (host, port))
    success = False
    try:
        smtp = smtplib.SMTP(host, port)
        header = 'From: %s\n' % sender
        header += 'To: %s\n' % ','.join(to_addr_list)
        if cc_addr_list:
            header += 'Cc: %s\n' % ','.join(cc_addr_list)
        if subject:
            header += 'Subject: %s\n\n' % subject
        msg = header + msg_body
        smtp.sendmail(sender, to_addr_list, msg)
        success = True
        logger.info(
            'Success: Email with subject [' +
            subject +
            '] was sent to:' +
            str(to_addr_list))
    except SMTPException as smtpe:
        logger.error("Unable to send email with subject [{0}] to {1} due: {2}" \
            .format(subject, str(to_addr_lista), str(smtpe)))
        logger.info("Please check if the recipient email is valid")
    except Exception as e:
        logger.error("Unable to send email with subject [{0}] to {1}\n due: {2}" \
            .format(subject, str(to_addr_list), str(e)))
        logger.info("Please check if the smtp server is configured properly")
    return success
