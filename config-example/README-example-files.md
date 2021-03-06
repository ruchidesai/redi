# Example Configuration Files

The configuration file examples provided here will allow you to test RED-I to push data into a sample REDCap project.  To use these files you will need access to a running REDCap server with the appropriate example project, and an API Token for that project that allows you to write to the project.  


## Getting REDCap

Research Electronic Data Capture (REDCap) is a software package written and distributed by Vanderbilt University.  If you do not already have a access to a REDCap system see http://project-redcap.org/ for details on how to become a consortium partner.  

Your institution may already provide you with access to REDCap.  If so you can use that access to create a test project.  With that, some assistance from your technical staff, and a few edits of the example files, you can test REDI.

REDI also includes the ability to create a REDCap server inside a virtual machine running on your own computer.  For more details on that option see ../vagrant/README.md.


## Getting the Right REDCap Project to use these files

This example configuration is based on the one of the default REDCap example projects.  This project is identified as "Longitudinal Database (1 arm)" in the REDCap template library.  In fresh REDCap installations like you will find in the test virtual machine, the project named "Example Database (Longitudinal)" has already been created for you using this template.  

## File Descriptions:

### settings.ini:

This file contains settings necessary to run REDI. It contains detailed descriptions of the fields which need to be set before running REDI.

### research_id_to_redcap_id_map.xml:

This file contains mappings of primary keys of your REDCap system and your custom project. This file is used by REDI at runtime to map your incoming project specific Id's to that of REDCap Id's.

### translationTable.xml:

This file maps your project specific component id's with REDCap Fields. Change this file to map your project specific component id's to REDCap Fields.

### formEvents.xml:

This file contains details of the form, events and fields which are updated by running REDI. If you have any forms to be updated, please add them in this file before running REDI.

### report.xsl:

This file is used for formatting the final REDI run report, which is sent to the receiver_email set in the settings.ini

### clinical-component-to-loinc-example.xml:

This file maps your project specific component id's to standard LOINC codes. For every new form added to formEvents.xml make sure that component id's of fields in that form are mapped to standard LOINC codes in this file.

