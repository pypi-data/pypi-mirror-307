# inspy package
inspy is a package that can automatically scan and control instruments which are supported SCPI COMMAND

version 0.1.8 supported DMM SMU Electronic Load and Power Suppy include( RUGOL: DP821A, DP831A, DL3021A GWINSTEK: GDM-9061, GDM-9060, GPP-6030 Keysight: 34461A Keithley: 2450, 2460)
version 0.1.8 uptated a bug
## Usage
    1. creat a pyvia ResourceManager (rm = pyvisa.ResourceManager())
    2. creat PiIns object (ins = PiIns(prm, pInsType, pInsName, pInsID) demo: dmm = PiIns(rm, "DMM", "9061", 'USB0::0x2184::0x0059::<SN>::INSTR'))
    3. read apis in ins_class.py to control instruments
    4. if want to scan instruments automatically please read demo in test/insdemo.py
    5. if want to add other instruments please add command and name in ins.json and insconst.py and update your own api in ins_class.py