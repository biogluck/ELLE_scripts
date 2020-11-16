# coding: utf8
import os
import csv
import arcpy


EC_DICT = {
        "1210": "Viengadīgu augu sabiedrības uz sanesumu joslām",
        "1220": "Daudzgadīgs augājs akmeņainās pludmalēs",
        "1230": "Jūras stāvkrasti",
        "1310": "Viengadīgu augu sabiedrības dūņainās un zemās smilšainās pludmalēs",
        "1640": "Smilšainas pludmales ar daudzgadīgu augāju",
        "2110": "Embrionālās kāpas",
        "2120": "Priekškāpas",
        "2170": "Pelēkās kāpas ar ložņu kārklu",
        "2180": "Mežainas piejūras kāpas",
        "2190": "Mitras starpkāpu ieplakas",
        "2320": "Piejūras zemienes smiltāju līdzenumu sausi virsāji",
        "2330": "Klajas iekšzemes kāpas",
        "3130": "Ezeri ar oligotrofām līdz mezotrofām augu sabiedrībām",
        "3140": "Ezeri ar mieturaļģu augāju",
        "3150": "Eitrofi ezeri ar iegrimušo ūdensaugu un peldaugu augāju",
        "3160": "Distrofi ezeri",
        "3260": "Upju straujteces un dabiski upju posmi",
        "4010": "Slapji virsāji",
        "4030": "Sausi virsāji",
        "5130": "Kadiķu audzes zālājos un virsājos",
        "6210": "Sausi zālāji kaļķainās augsnēs",
        "6410": "Mitri zālāji periodiski izžūstošās augsnēs",
        "6430": "Eitrofas augsto lakstaugu audzes",
        "6450": "Palieņu zālāji",
        "6510": "Mēreni mitras pļavas",
        "7120": "Degradēti augstie purvi, kuros iespējama vai noris dabiskā atjaunošanās",
        "7140": "Pārejas purvi un slīkšņas",
        "7150": "Rhynchosporion albae pioniersabiedrības uz mitras kūdras vai smiltīm",
        "7160": "Minerālvielām bagāti avoti un avotu purvi",
        "7230": "Kaļķaini zāļu purvi",
        "8210": "Karbonātisku pamatiežu atsegumi",
        "8220": "Smilšakmens atsegumi",
        "8310": "Netraucētas alas",
        "9050": "Lakstaugiem bagāti egļu meži",
        "9060": "Skujkoku meži uz osveida reljefa formām",
        "9070": "Meža ganības",
        "9160": "Ozolu meži (ozolu, liepu un skābaržu meži)",
        "1630*": "Piejūras zālāji",
        "2130*": "Ar lakstaugiem klātas pelēkās kāpas",
        "2140*": "Pelēkās kāpas ar sīkkrūmu audzēm",
        "6110*": "Lakstaugu pioniersabiedrības seklās kaļķainās augsnēs",
        "6120*": "Smiltāju zālāji",
        "6230*": "Vilkakūlas zālāji (tukšaiņu zālāji)",
        "6270*": "Sugām bagātas ganības un ganītas pļavas",
        "6530*": "Parkveida pļavas un ganības",
        "7110*": "Aktīvi augstie purvi",
        "7210*": "Dižās aslapes Cladium mariscus audzes ezeros un purvos",
        "7220*": "Avoti, kas izgulsnē avotkaļķus",
        "9010*": "Veci vai dabiski boreāli meži",
        "9020*": "Veci jaukti platlapju meži",
        "9080*": "Staignāju meži",
        "9180*": "Nogāžu un gravu meži",
        "91D0*": "Purvaini meži",
        "91E0*": "Aluviāli meži (aluviāli krastmalu un palieņu meži)",
        "91F0": "Jaukti ozolu, gobu, ošu meži gar lielām upēm",
        "91T0": "Ķērpjiem bagāti priežu meži",
        "3270": "Dūņaini upju krasti ar slāpekli mīlošu viengadīgu pioniersugu augāju",
        "3190*": "Karsta kritenes",
        "1150*": "Lagūnas",
    }

def get_experts(csv_file):
    experts = {}
    with open(csv_file, 'r') as f:
        csv_reader = csv.reader(f, delimiter='\t') 
        next(csv_reader)
        for line in csv_reader:
            experts[line[0]] = line[1]
    return experts

WORKDIR = os.getcwd()
# experts.csv should have name in 1st column and code in 2nd
experts_file = os.path.join(WORKDIR, 'experts.csv')
experts = get_experts(experts_file)

def update_fields(fc):
    cursor = arcpy.UpdateCursor(fc)
    for row in cursor:
        form_number = row.getValue("FORM_NUMBER")
        if row.getValue("OBSERVER"):
            expert_name = row.getValue("OBSERVER").encode("utf-8")
        polygon_number = row.getValue("POLYGON_NUMBER")
        not_ec = row.getValue("NOT_EC")
        ec_code = row.getValue("CODE_EC")
        ec_name = EC_DICT.get(ec_code)
        if ec_name:
            row.setValue("NAME_EC", ec_name)
        if expert_name:
            expert_code = experts.get(expert_name)
        if not polygon_number:
            print "no poly number"
            return
        if polygon_number.isdigit():
            print "setting new polygon number"
            new_polygon_number = expert_code + "_" + str(polygon_number)
            row.setValue("POLYGON_NUMBER", new_polygon_number)
            cursor.updateRow(row)
        if form_number:
            if form_number.count("_") == 1:
                # if has form_number without expert prefix
                new_form_number = expert_code + "_" + form_number
                row.setValue("FORM_NUMBER", new_form_number)
                cursor.updateRow(row)   
        else:
            if polygon_number and polygon_number.isdigit() and not not_ec:
                new_form_number = expert_code + '_' + polygon_number + '_1'
                row.setValue("FORM_NUMBER", new_form_number)
                cursor.updateRow(row)


for path in os.listdir(WORKDIR):
    if path.endswith('.gdb'):
        fc = os.path.join(WORKDIR, path )+ "\Habitat_poly"
        print 'Updating fields for {}'.format(fc)
        update_fields(fc)
        print "="*70
