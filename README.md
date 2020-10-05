# ClickIt
Team ClickIt Github repo.

### Installation
#### Install Odoo
* [Odoo Installation Guide](https://www.odoo.com/documentation/master/setup/install.html#source-install)
    * The installation **WILL NOT WORK** if you are using Python 3.8+. We recommend using Python 3.6.x

#### Install Our Module
1. Open a terminal (in administrator mode, if relevant) at the root of your Odoo installation.
2. In your terminal, run the following command:
    * UNIX:  
    `python3 odoo-bin --addons-path=addons -d odoo_db -i base`
    * Windows:   
    `python odoo-bin -w odoo -r odoo --addons-path=addons -d odoo_db -i base`
3. In step 2, we launched odoo with the argument `-d odoo_db`. This allowed odoo to properly initialize, but unfortunately we cannot log in using that database. In your browser, go to `localhost:8069`. 

![Odoo Login Page](https://github.com/jsalajka/images/blob/main/odoo_landing_page.png)

4. On the Odoo login page, click Manage Databases.
5. Create a Master Password, then click "Create Database". 
6. Choose any name for the database EXCEPT `odoo_db`. You will need to check the "Demo Data" box.
7. Stop the odoo process in your terminal. Once it is stopped, run the following command:
    * `git clone https://github.com/whagan/custom_addons.git`
8. Start odoo again with the following command:
    * UNIX:  
    `python3 odoo-bin --addons-path=addons,custom_addons -d DATABASE_NAME -u custom_reports`
    * Windows:  
    `python odoo-bin -w odoo -r odoo --addons-path=addons,custom_addons -d DATABASE_NAME -u custom_reports`  
9. You can now log in with the email and password you chose earlier.
10. Install the Odoo "Point of Sale", "Employees", and "Attendance" modules.
If you are not already in the "Apps" menu, click the Menu button in the top left to open a dropdown menu, then click "Apps".

![Install Sales Module](https://github.com/jsalajka/images/blob/main/install_attendances_module.png)

11. Install the ClickIt "Custom Reports" module the same way.
