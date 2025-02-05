from design_type.member import Member
from Common import *
from utils.common.component import ISection, Material
from utils.common.common_calculation import *
from utils.common.load import Load
from design_type.tension_member import *
from utils.common.Section_Properties_Calculator import I_sectional_Properties
import math
import numpy as np
from utils.common import is800_2007
from utils.common.component import *



class Compression(Member):

    def __init__(self):
        print(f"Here Compression")
        super(Compression, self).__init__()

    ###############################################
    # Design Preference Functions Start
    ###############################################
    def tab_list(self):
        """

        :return: This function returns the list of tuples. Each tuple will create a tab in design preferences, in the
        order they are appended. Format of the Tuple is:
        [Tab Title, Type of Tab, function for tab content)
        Tab Title : Text which is displayed as Title of Tab,
        Type of Tab: There are Three types of tab layouts.
            Type_TAB_1: This have "Add", "Clear", "Download xlsx file" "Import xlsx file"
            TYPE_TAB_2: This contains a Text box for side note.
            TYPE_TAB_3: This is plain layout
        function for tab content: All the values like labels, input widgets can be passed as list of tuples,
        which will be displayed in chosen tab layout

        """
        tabs = []

        t1 = (KEY_DISP_COLSEC, TYPE_TAB_1, self.tab_section)
        tabs.append(t1)

        t5 = ("Design", TYPE_TAB_2, self.design_values)
        tabs.append(t5)

        return tabs

    def tab_value_changed(self):
        """

        :return: This function is used to update the values of the keys in design preferences,
         which are dependent on other inputs.
         It returns list of tuple which contains, tab name, keys whose values will be changed,
         function to change the values and arguments for the function.

         [Tab Name, [Argument list], [list of keys to be updated], input widget type of keys, change_function]

         Here Argument list should have only one element.
         Changing of this element,(either changing index or text depending on widget type),
         will update the list of keys (this can be more than one).
         TODO: input widget type of keys (3rd element) is no longer required. needs to be removed

         """
        change_tab = []
    #
    #     t1 = (KEY_DISP_COLSEC, [KEY_SECSIZE, KEY_SEC_MATERIAL],
    #           [KEY_SECSIZE_SELECTED, KEY_SEC_FY, KEY_SEC_FU, 'Label_1', 'Label_2', 'Label_3', 'Label_4', 'Label_5',
    #            'Label_7', 'Label_11', 'Label_12', 'Label_13', 'Label_14', 'Label_15', 'Label_16', 'Label_17',
    #            'Label_18', 'Label_19', 'Label_20', 'Label_21', 'Label_22', KEY_IMAGE], TYPE_TEXTBOX,
    #           self.get_new_angle_section_properties)
    #     change_tab.append(t1)
    #
    #     t2 = (DISP_TITLE_ANGLE, ['Label_1', 'Label_2', 'Label_3', 'Label_0'],
    #           ['Label_7', 'Label_8', 'Label_9', 'Label_10', 'Label_11', 'Label_12', 'Label_13', 'Label_14',
    #            'Label_15',
    #            'Label_16', 'Label_17', 'Label_18', 'Label_19', 'Label_20', 'Label_21', 'Label_22', 'Label_23',
    #            KEY_IMAGE],
    #           TYPE_TEXTBOX, self.get_Angle_sec_properties)
    #     change_tab.append(t2)
    #
    #     t6 = (DISP_TITLE_ANGLE, [KEY_SECSIZE_SELECTED], [KEY_SOURCE], TYPE_TEXTBOX, self.change_source)
    #     change_tab.append(t6)
    #
    #     t7 = (DISP_TITLE_CHANNEL, [KEY_SECSIZE_SELECTED], [KEY_SOURCE], TYPE_TEXTBOX, self.change_source)
    #     change_tab.append(t7)
    #
        return change_tab

    def edit_tabs(self):
        """ This function is required if the tab name changes based on connectivity or profile or any other key.
                Not required for this module but empty list should be passed"""
        return []

    def input_dictionary_design_pref(self):
        """

        :return: This function is used to choose values of design preferences to be saved to design dictionary.

         It returns list of tuple which contains, tab name, input widget type of keys, keys whose values to be saved,

         [(Tab Name, input widget type of keys, [List of keys to be saved])]

         """
        design_input = []

        t2 = (KEY_DISP_COLSEC, TYPE_COMBOBOX, [KEY_SEC_MATERIAL])
        design_input.append(t2)

        t7 = ("Connector", TYPE_COMBOBOX, [KEY_CONNECTOR_MATERIAL])
        design_input.append(t7)

        return design_input

    def input_dictionary_without_design_pref(self):
        """

        :return: This function is used to choose values of design preferences to be saved to
        design dictionary if design preference is never opened by user. It sets are design preference values to default.
        If any design preference value needs to be set to input dock value, tuple shall be written as:

        (Key of input dock, [List of Keys from design prefernce], 'Input Dock')

        If the values needs to be set to default,

        (None, [List of Design Prefernce Keys], '')

         """
        design_input = []
        t1 = (KEY_MATERIAL, [KEY_SEC_MATERIAL], 'Input Dock')
        design_input.append(t1)

        t2 = (None, [KEY_DP_DESIGN_METHOD], '')
        design_input.append(t2)

        t2 = (None, [KEY_ALLOW_UR, KEY_EFFECTIVE_AREA_PARA, KEY_OPTIMIZATION_PARA, KEY_ALLOW_CLASS1, KEY_ALLOW_CLASS2, KEY_ALLOW_CLASS3,
                     KEY_ALLOW_CLASS4, KEY_STEEL_COST, KEY_DP_DESIGN_METHOD], '')
        design_input.append(t2)

        return design_input

    def refresh_input_dock(self):
        """

        :return: This function returns list of tuples which has keys that needs to be updated,
         on changing Keys in design preference (ex: adding a new section to database should reflect in input dock)

         [(Tab Name,  Input Dock Key, Input Dock Key type, design preference key, Master key, Value, Database Table Name)]
        """
        add_buttons = []

        # t2 = (KEY_DISP_COLSEC, KEY_SECSIZE, TYPE_COMBOBOX, KEY_SECSIZE, None, None, "Columns")
        # add_buttons.append(t2)

        t2 = (DISP_TITLE_ANGLE, KEY_SECSIZE, TYPE_COMBOBOX_CUSTOMIZED, KEY_SECSIZE_SELECTED, KEY_SEC_PROFILE,
              ['Angles', 'Back to Back Angles'], "Angles")
        add_buttons.append(t2)

        t2 = (DISP_TITLE_CHANNEL, KEY_SECSIZE, TYPE_COMBOBOX_CUSTOMIZED, KEY_SECSIZE_SELECTED, KEY_SEC_PROFILE,
              ['Channels', 'Back to Back Channels'], "Channels")
        add_buttons.append(t2)

        return add_buttons

    def get_values_for_design_pref(self, key, design_dictionary):

        if design_dictionary[KEY_MATERIAL] != 'Select Material':
            material = Material(design_dictionary[KEY_MATERIAL], 41)
            fu = material.fu
            fy = material.fy
        else:
            fu = ''
            fy = ''

        val = {
            KEY_ALLOW_UR: '1.0',
            KEY_EFFECTIVE_AREA_PARA: '1.0',
            KEY_OPTIMIZATION_PARA: 'Utilization Ratio',
            KEY_STEEL_COST: '50',
            KEY_ALLOW_CLASS1: 'Yes',
            KEY_ALLOW_CLASS2: 'Yes',
            KEY_ALLOW_CLASS3: 'Yes',
            KEY_ALLOW_CLASS4: 'Yes',
            KEY_DP_DESIGN_METHOD: "Limit State Design",
               }[key]

        return val

    ####################################
    # Design Preference Functions End
    ####################################

    def module_name(self):
        return KEY_DISP_COMPRESSION

    def set_osdaglogger(key):

        """
        Function to set Logger for FinPlate Module
        """

        # @author Arsil Zunzunia
        global logger
        logger = logging.getLogger('osdag')

        logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler()
        # handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%H:%M:%S')

        handler.setFormatter(formatter)
        logger.addHandler(handler)
        handler = logging.FileHandler('logging_text.log')

        # handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%H:%M:%S')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        # handler.setLevel(logging.INFO)
        # formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%H:%M:%S')
        # handler.setFormatter(formatter)
        # logger.addHandler(handler)
        if key is not None:
            handler = OurLog(key)
            # handler.setLevel(logging.DEBUG)
            formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%H:%M:%S')
            handler.setFormatter(formatter)
            logger.addHandler(handler)

    def customized_input(self):

        c_lst = []

        t1 = (KEY_SECSIZE, self.fn_profile_section)
        c_lst.append(t1)

        return c_lst

    def input_values(self):

        '''
        Fuction to return a list of tuples to be displayed as the UI.(Input Dock)
        '''

        # @author: Amir, Umair

        options_list = []

        t1 = (KEY_MODULE, KEY_DISP_COMPRESSION_Strut, TYPE_MODULE, None, True, 'No Validator')
        options_list.append(t1)

        t1 = (None, KEY_SECTION_DATA, TYPE_TITLE, None, True, 'No Validator')
        options_list.append(t1)

        t2 = (KEY_SEC_PROFILE, KEY_DISP_SEC_PROFILE, TYPE_COMBOBOX, VALUES_SEC_PROFILE_Compression_Strut, True, 'No Validator')
        options_list.append(t2)

        t3 = (KEY_IMAGE, None, TYPE_IMAGE, VALUES_IMG_TENSIONBOLTED[0], True, 'No Validator')
        options_list.append(t3)
#([KEY_SEC_PROFILE], KEY_IMAGE, TYPE_IMAGE, self.fn_conn_image)

        t4 = (KEY_SECSIZE, KEY_DISP_SECSIZE, TYPE_COMBOBOX_CUSTOMIZED, ['All','Customized'], True, 'No Validator')
        options_list.append(t4)

        t4 = (KEY_MATERIAL, KEY_DISP_MATERIAL, TYPE_COMBOBOX, VALUES_MATERIAL, True, 'No Validator')
        options_list.append(t4)

        t5 = (KEY_LENGTH, KEY_DISP_LENGTH, TYPE_TEXTBOX, None, True, 'Int Validator')
        options_list.append(t5)


        # t6 = (KEY_LENYY, KEY_DISP_LENYY, TYPE_TEXTBOX, None, True, 'No Validator')
        # options_list.append(t6)

        

        # t12 = (KEY_MOMENT_MAJOR, KEY_DISP_MOMENT_MAJOR, TYPE_TEXTBOX, None, True, 'No Validator')
        # options_list.append(t12)
        #
        # t13 = (KEY_MOMENT_MINOR, KEY_DISP_MOMENT_MINOR, TYPE_TEXTBOX, None, True, 'No Validator')
        # options_list.append(t13)

        t9 = (None, DISP_TITLE_SC, TYPE_TITLE, None, True, 'No Validator')
        options_list.append(t9)

        t10 = (KEY_END1, KEY_DISP_END1, TYPE_NOTE, VALUES_STRUT_END1, True, 'No Validator')
        options_list.append(t10)

        t11 = (KEY_END2, KEY_DISP_END2, TYPE_NOTE, VALUES_STRUT_END2, True, 'No Validator')
        options_list.append(t11)

        t12 = (KEY_IMAGE, None, TYPE_IMAGE_COMPRESSION, "./ResourceFiles/images/3.RFRF.PNG", True, 'No Validator')
        options_list.append(t12)

        t7 = (None, DISP_TITLE_FSL, TYPE_TITLE, None, True, 'No Validator')
        options_list.append(t7)

        t8 = (KEY_AXIAL, KEY_DISP_AXIAL, TYPE_TEXTBOX, None, True, 'No Validator')
        options_list.append(t8)

        return options_list

    def fn_conn_image(self):

        "Function to populate section images based on the type of section "
        img = self[0]
        if img == VALUES_SEC_PROFILE_Compression_Strut[0]:
            return VALUES_IMG_TENSIONBOLTED[0]
        elif img ==VALUES_SEC_PROFILE_Compression_Strut[1]:
            return VALUES_IMG_TENSIONBOLTED[1]
        elif img ==VALUES_SEC_PROFILE_Compression_Strut[2]:
            return VALUES_IMG_TENSIONBOLTED[3]
        else:
            return VALUES_IMG_TENSIONBOLTED[4]

    def fn_profile_section(self):

        profile = self[0]
        print(f'profile = {self[0]}')
        if profile == 'Beams':
            return connectdb("Beams", call_type="popup")
        elif profile == 'Columns':
            return connectdb("Columns", call_type="popup")
        elif profile == 'RHS':
            return connectdb("RHS", call_type="popup")
        elif profile == 'SHS':
            return connectdb("SHS", call_type="popup")
        elif profile == 'CHS':
            return connectdb("CHS", call_type="popup")
        elif profile in ['Angles', 'Back to Back Angles']:
            return connectdb("Angles", call_type="popup")
        elif profile in ['Channels', 'Back to Back Channels']:
            return connectdb("Channels", call_type="popup")


    # def fn_end1_end2(self):
    #
    #     end1 = self[0]
    #     if end1 == 'Fixed':
    #         return VALUES_END2
    #     elif end1 == 'Free':
    #         return ['Fixed']
    #     elif end1 == 'Hinged':
    #         return ['Fixed', 'Hinged', 'Roller']
    #     elif end1 == 'Roller':
    #         return ['Fixed', 'Hinged']

    # def fn_end1_image(self):
    #
    #     if self == 'Fixed':
    #         return "./ResourceFiles/images/6.RRRR.PNG"
    #     elif self == 'Free':
    #         return "./ResourceFiles/images/1.RRFF.PNG"
    #     elif self == 'Hinged':
    #         return "./ResourceFiles/images/5.RRRF.PNG"
    #     elif self == 'Roller':
    #         return "./ResourceFiles/images/4.RRFR.PNG"

    # def fn_end2_image(self):
    #
    #     end1 = self[0]
    #     end2 = self[1]
    #
    #     if end1 == 'Fixed':
    #         if end2 == 'Fixed':
    #             return "./ResourceFiles/images/6.RRRR.PNG"
    #         elif end2 == 'Free':
    #             return "./ResourceFiles/images/1.RRFF_rotated.PNG"
    #         elif end2 == 'Hinged':
    #             return "./ResourceFiles/images/5.RRRF_rotated.PNG"
    #         elif end2 == 'Roller':
    #             return "./ResourceFiles/images/4.RRFR_rotated.PNG"
    #     elif end1 == 'Free':
    #         return "./ResourceFiles/images/1.RRFF.PNG"
    #     elif end1 == 'Hinged':
    #         if end2 == 'Fixed':
    #             return "./ResourceFiles/images/5.RRRF.PNG"
    #         elif end2 == 'Hinged':
    #             return "./ResourceFiles/images/3.RFRF.PNG"
    #         elif end2 == 'Roller':
    #             return "./ResourceFiles/images/2.FRFR_rotated.PNG"
    #     elif end1 == 'Roller':
    #         if end2 == 'Fixed':
    #             return "./ResourceFiles/images/4.RRFR.PNG"
    #         elif end2 == 'Hinged':
    #             return "./ResourceFiles/images/2.FRFR.PNG"

    def input_value_changed(self):

        lst = []

        t1 = ([KEY_SEC_PROFILE], KEY_SECSIZE, TYPE_COMBOBOX_CUSTOMIZED, self.fn_profile_section)
        lst.append(t1)

        # t2 = ([KEY_END1], KEY_END2, TYPE_COMBOBOX, self.fn_end1_end2)
        # lst.append(t2)

        t3 = ([KEY_SEC_PROFILE], KEY_IMAGE, TYPE_IMAGE, self.fn_conn_image)
        lst.append(t3)

        # t3 = ([KEY_END1, KEY_END2], KEY_IMAGE, TYPE_IMAGE, self.fn_end2_image)
        # lst.append(t3)

        # t4 = (KEY_END2, KEY_IMAGE, TYPE_IMAGE, self.fn_end2_image)
        # lst.append(t4)
        print(f'input_value_changed lst={lst}')
        return lst

    def output_values(self,flag):
        out_list = []
        t1 = (None, DISP_TITLE_TENSION_SECTION, TYPE_TITLE, None, True)
        out_list.append(t1)

        return out_list
    def func_for_validation(self, design_dictionary):
        '''Need to check'''
        all_errors = []
        self.design_status = False
        flag = False
        option_list = self.input_values(self)
        print(f'\n func_for_validation option list = {option_list}')
        missing_fields_list = []
        for option in option_list:
            if option[2] == TYPE_TEXTBOX:
                if design_dictionary[option[0]] == '':
                    if design_dictionary[KEY_AXIAL] == '':
                        continue
                    else:
                        print(f'option[0] = {option[0]}')
                        missing_fields_list.append(option[1])
            elif option[2] == TYPE_COMBOBOX and option[0] not in [KEY_SEC_PROFILE, KEY_END1, KEY_END2]:
                val = option[3]
                if design_dictionary[option[0]] == val[0]:
                    print(f'option[0] = {option[0]}')
                    missing_fields_list.append(option[1])

        if len(missing_fields_list) > 0:

            error = self.generate_missing_fields_error_string(self,missing_fields_list)
            all_errors.append(error)
            # flag = False
        else:
            flag = True

        print(f'flag = {flag}')
        if flag:
            self.set_input_values(self, design_dictionary)
            # print(design_dictionary)
        else:
            return all_errors

    # Setting inputs from the input dock GUI

    def set_input_values(self, design_dictionary):
        super(Compression,self).set_input_values(self, design_dictionary)

        #self.sizelist == self.sec_list

        # section properties
        self.module = design_dictionary[KEY_MODULE]
        self.sizelist = design_dictionary[KEY_SECSIZE]
        self.sec_profile = design_dictionary[KEY_SEC_PROFILE]
        self.sec_list = design_dictionary[KEY_SECSIZE]
        self.length = float(design_dictionary[KEY_LENGTH])
        self.main_material = design_dictionary[KEY_MATERIAL]
        self.material = design_dictionary[KEY_SEC_MATERIAL]

        self.loc = 'Long Leg'

        # end condition
        self.end_1 = design_dictionary[KEY_END1]
        self.end_2 = design_dictionary[KEY_END2]

        # self.length_zz = float(design_dictionary[KEY_LENZZ])
        # self.length_yy = float(design_dictionary[KEY_LENYY])

        # factored loads
        self.load = Load(shear_force="", axial_force=design_dictionary[KEY_AXIAL],moment="",unit_kNm=True)
        #  moment=design_dictionary[KEY_MOMENT_MAJOR]
        #                  moment_minor = design_dictionary[KEY_MOMENT_MINOR],unit_kNm=True)
        print(f"set_input_values design_dictionary {design_dictionary}")
        print(f"set_input_values self.module {self.module}")
        print(f"set_input_values self.sec_profile {self.sec_profile}")
        print(f"set_input_values self.material {self.material}")
        # print(f"set_input_values self.length_yy {self.length_yy}")
        print(f"set_input_values self.load {self.load}")

        # design preferences
        self.allowable_utilization_ratio = float(design_dictionary[KEY_ALLOW_UR])
        self.effective_area_factor = float(design_dictionary[KEY_EFFECTIVE_AREA_PARA])
        self.optimization_parameter = design_dictionary[KEY_OPTIMIZATION_PARA]
        self.allow_class1 = design_dictionary[KEY_ALLOW_CLASS1]
        self.allow_class2 = design_dictionary[KEY_ALLOW_CLASS2]
        self.allow_class3 = design_dictionary[KEY_ALLOW_CLASS3]
        self.allow_class4 = design_dictionary[KEY_ALLOW_CLASS4]
        self.steel_cost_per_kg = float(design_dictionary[KEY_STEEL_COST])

        self.allowed_sections = []

        if self.allow_class1 == "Yes":
            self.allowed_sections.append('Plastic')
        if self.allow_class2 == "Yes":
            self.allowed_sections.append('Compact')
        if self.allow_class3 == "Yes":
            self.allowed_sections.append('Semi-Compact')
        '''Need to check'''
        if self.allow_class4 == "Yes":
            self.allowed_sections.append('Slender')
        
        print(f"self.allowed_sections {self.allowed_sections}")
        print("==================")
        print(f"self.module{self.module}")
        print(f"self.sec_list {self.sec_list}")
        print(f"self.sec_profile {self.sec_profile}")
        print(f"self.material {self.material}")
        print(f"self.length {self.length}")
        print(f"self.load {self.load}")
        print(f"self.end_1,2 {self.end_1}, {self.end_2}")
        print("==================")
        # print(self.length_zz)
        # Assuming first member as selected size
        # selectedsize = design_dictionary[KEY_SECSIZE][0]
                # safety factors
        self.gamma_m0 = IS800_2007.cl_5_4_1_Table_5["gamma_m0"]["yielding"]
        # material property
        self.material_property = Material(material_grade=self.material, thickness=0)
        print(f"self.material_property {self.material_property}]")

        # initialize the design status
        self.design_status_list = []
        self.design_status = False

        self.design_classification(self)
        if design_dictionary[KEY_AXIAL] == '':
            self.strength_of_strut(self)
        else:
            self.design_strut(self)
        # self.results(self)
        print(f"Here[Compression/set_input_values]")

        "Unknown keys"
        self.efficiency = 0.0
        self.K = 1
        self.plate = Plate(thickness=['10'],
                           material_grade='E 250 (Fe 410 W)A')
        self.count = 0
        self.member_design_status = False
        self.max_limit_status_1 = False
        self.max_limit_status_2 = False
        self.bolt_design_status = False
        self.plate_design_status = False
        # self.inter_status = False
        self.thk_count =0

        print("The input values are set. Performing preliminary member check(s).")
        # self.i = 0

        # self.initial_member_capacity(self,design_dictionary)
        self.select_section(self,self.sec_list, design_dictionary)

    def select_section(self, selectedsize, design_dictionary):

        "selecting components class based on the section passed "
        print(f" \n select_section started \n")

        if design_dictionary[KEY_SEC_PROFILE] in ['Angles', 'Back to Back Angles', 'Star Angles']:
            self.section_size = Angle(designation=selectedsize, material_grade=design_dictionary[KEY_SEC_MATERIAL])
        else:
            pass
        print(f"\n select_section done \n")
        
        return self.section_size
        print(self.selectedsize)

    # Simulation starts here
    def design_classification(self):
        """ Classify the sections based on Table 2 of IS 800:2007 """
        self.input_section_list = []
        self.input_section_classification = {}

        print(f"self.sec_list {self.sec_list}")

        for section in self.sec_list:
            trial_section = section.strip("'")
            # print(f"trial_section  {trial_section}")

    def initial_member_capacity(self,design_dictionary,previous_size = None):

        "selection of member based on the yield capacity"
        min_yield = 0

        if self.count == 0:
            self.max_section(self,design_dictionary,self.sizelist)
            [self.force1, self.len1, self.slen1, self.gyr1]= self.max_force_length(self,  self.max_area)
            [self.force2, self.len2, self.slen2, self.gyr2] = self.max_force_length(self,  self.max_gyr)
        else:
            pass

        self.count = self.count + 1
        "Loop checking each member from sizelist based on yield capacity"
        if (previous_size) == None:
            pass
        else:
            if previous_size in self.sizelist:
                self.sizelist.remove(previous_size)
            else:
                pass
        for selectedsize in self.sizelist:
            # print('selectedsize',self.sizelist)
            self.section_size = self.select_section(self,design_dictionary,selectedsize)
            self.bolt_diameter_min= min(self.bolt.bolt_diameter)

            self.edge_dist_min = IS800_2007.cl_10_2_4_2_min_edge_end_dist(self.bolt_diameter_min,self.bolt.bolt_hole_type,
                                                                          'machine_flame_cut')
            self.d_0_min = IS800_2007.cl_10_2_1_bolt_hole_size(self.bolt_diameter_min,
                                                                          design_dictionary[KEY_DP_BOLT_HOLE_TYPE])

            self.edge_dist_min_round = round_up(self.edge_dist_min, 5)
            self.pitch_round = round_up((2.5*self.bolt_diameter_min), 5)
            if design_dictionary[KEY_SEC_PROFILE] in ['Channels', 'Back to Back Channels']:
                 self.max_depth = self.section_size_max.max_plate_height()
            else:
                if self.loc == "Long Leg":
                    self.max_depth =self.section_size_max.max_leg - self.section_size_max.thickness - self.section_size_max.root_radius
                else:
                    self.max_depth =self.section_size_max.min_leg - self.section_size_max.thickness - self.section_size_max.root_radius


            "selection of minimum member size required based on the miniumum size of bolt  in bolt diameter list "

            if design_dictionary[KEY_LOCATION] == "Long Leg":
               if self.section_size.max_leg < self.section_size.root_radius + self.section_size.thickness + (2 *self.edge_dist_min_round):
                   continue
            elif design_dictionary[KEY_LOCATION] == 'Short Leg':
                if self.section_size.min_leg < self.section_size.root_radius + self.section_size.thickness + (2 * self.edge_dist_min_round ):
                    continue
            if design_dictionary[KEY_SEC_PROFILE] =='Channels':
                self.max_plate_height = self.section_size.max_plate_height()
                if self.max_plate_height < (self.pitch_round) + (2 * self.edge_dist_min_round):
                    continue
                else:
                    self.cross_area = self.section_size.area

            elif design_dictionary[KEY_SEC_PROFILE] == 'Back to Back Channels':
                self.max_plate_height = self.section_size.max_plate_height()
                if self.max_plate_height < (self.pitch_round) + (2 * self.edge_dist_min_round):
                    continue
                else:
                    self.cross_area = self.section_size.area * 2

            elif design_dictionary[KEY_SEC_PROFILE] =='Angles':
                self.cross_area = self.section_size.area

            else:
                self.cross_area = self.section_size.area * 2

            "excluding previous section size which failed in rupture and selecting higher section based on the cross section area "

            self.section_size.tension_member_yielding(A_g = self.cross_area , F_y =self.section_size.fy)
            self.K = 1.0
            # print(self.section_size.rad_of_gy_z)
            if design_dictionary[KEY_SEC_PROFILE] in ['Angles','Star Angles','Back to Back Angles']:
                # print(selectedsize)
                self.min_rad_gyration_calc(self,designation=self.section_size.designation, material_grade=self.material,
                                           key=self.sec_profile, subkey=self.loc, D_a=self.section_size.a,
                                           B_b=self.section_size.b, T_t=self.section_size.thickness)
            else:
                self.min_rad_gyration_calc(self,designation=self.section_size.designation, material_grade=self.material,
                                           key=self.sec_profile, subkey=self.loc, D_a=self.section_size.depth,
                                           B_b=self.section_size.flange_width, T_t=self.section_size.flange_thickness,
                                           t=self.section_size.web_thickness)
            # print(design_dictionary[KEY_SEC_PROFILE], design_dictionary[KEY_LOCATION], self.section_size.min_radius_gyration)
            self.section_size.design_check_for_slenderness(K=self.K, L=design_dictionary[KEY_LENGTH],r=self.min_radius_gyration)
                # print(self.section_size.tension_yielding_capacity)

            "condition for yield and slenderness check "

            if (self.section_size.tension_yielding_capacity >= self.load.axial_force*1000) and self.section_size.slenderness < 400:
                min_yield_current = self.section_size.tension_yielding_capacity
                self.member_design_status = True
                if min_yield == 0:
                    min_yield = min_yield_current
                    self.section_size_1 = self.select_section(self, design_dictionary, selectedsize)
                    self.section_size_1.tension_member_yielding(A_g=self.cross_area, F_y=self.section_size.fy)
                    if design_dictionary[KEY_SEC_PROFILE] in ['Angles', 'Star Angles', 'Back to Back Angles']:
                        self.min_rad_gyration_calc(self,designation=self.section_size_1.designation,
                                                   material_grade=self.material,
                                                   key=self.sec_profile, subkey=self.loc, D_a=self.section_size_1.a,
                                                   B_b=self.section_size_1.b, T_t=self.section_size_1.thickness)

                    else:
                        self.min_rad_gyration_calc(self,designation=self.section_size_1.designation,
                                                   material_grade=self.material,
                                                   key=self.sec_profile, subkey=self.loc, D_a=self.section_size_1.depth,
                                                   B_b=self.section_size_1.flange_width,
                                                   T_t=self.section_size_1.flange_thickness,
                                                   t=self.section_size_1.web_thickness)

                    self.section_size_1.design_check_for_slenderness(K=self.K, L=design_dictionary[KEY_LENGTH],
                                                               r=self.min_radius_gyration)

                elif min_yield_current < min_yield:
                    min_yield = min_yield_current
                    self.section_size_1 = self.select_section(self, design_dictionary, selectedsize)
                    self.section_size_1.tension_member_yielding(A_g=self.cross_area, F_y=self.section_size.fy)
                    if design_dictionary[KEY_SEC_PROFILE] in ['Angles', 'Star Angles', 'Back to Back Angles']:
                        self.min_rad_gyration_calc(self,designation=self.section_size_1.designation,
                                                   material_grade=self.material,
                                                   key=self.sec_profile, subkey=self.loc, D_a=self.section_size_1.a,
                                                   B_b=self.section_size_1.b, T_t=self.section_size_1.thickness)
                    else:
                        self.min_rad_gyration_calc(self,designation=self.section_size_1.designation,
                                                   material_grade=self.material,
                                                   key=self.sec_profile, subkey=self.loc, D_a=self.section_size_1.depth,
                                                   B_b=self.section_size_1.flange_width,
                                                   T_t=self.section_size_1.flange_thickness,
                                                   t=self.section_size_1.web_thickness)
                self.section_size_1.design_check_for_slenderness(K=self.K, L=design_dictionary[KEY_LENGTH],
                                                                 r=self.min_radius_gyration)

                # print(self.section_size_1.slenderness)

                "condition to limit loop based on max force derived from max available size."

            elif (self.load.axial_force*1000 > self.force1) :
                self.max_limit_status_1 = True
                # self.design_status = False
                logger.warning(" : The factored tension force ({} kN) exceeds the tension capacity ({} kN) with respect to the maximum available "
                               "member size {}.".format(round(self.load.axial_force,2),round(self.force1/1000,2),self.max_area))
                logger.info(" : Define member(s) with a higher cross sectional area.")
                # logge r.error(": Design is not safe. \n ")
                # logger.info(" :=========End Of design===========")
                break

                "condition to limit loop based on max length derived from max available size"

            elif self.length > self.len2:
                self.max_limit_status_2 = True
                # self.design_status = False
                logger.warning(" : The member length ({} mm) exceeds the maximum allowable length ({} mm) with respect to the maximum available "
                               "member size {}.".format(self.length,round(self.len2,2),self.max_gyr))
                logger.info(" : Select member(s) with a higher radius of gyration value.")
                # logger.error(": Design is not safe. \n ")
                # logger.info(" :=========End Of design===========")
                break

            else:
                pass

        if self.member_design_status == False and self.max_limit_status_1!=True and self.max_limit_status_2!=True:
            logger.warning(" : The available depth of the member cannot accommodate the minimum available bolt diameter of {} mm considering the "
                           "minimum spacing limit [Ref. Cl. 10.2, IS 800:2007].".format(self.bolt_diameter_min))
            logger.info(" : Reduce the bolt diameter or increase the member depth and re-design.")
            # logger.error(": Design is not safe. \n ")
            # logger.info(" :=========End Of design===========")

        if self.member_design_status == True:
            print("pass")
            self.design_status = True
            self.select_bolt_dia(self, design_dictionary)
        else:
            self.design_status = False
            logger.error(": Design is unsafe. \n ")
            logger.info(" :=========End Of design===========")




    def get_3d_components(self):

        components = []
        return components

#  ======Calculations start here====== #

    def design_strut(self):
            """ Perform design of struct """
            # checking DP inputs

            # if (self.allowable_utilization_ratio <= 0.10) or (self.allowable_utilization_ratio > 1.0):
            #     logger.warning("The defined value of Utilization Ratio in the design preferences tab is out of the suggested range.")
            #     logger.info("Provide an appropriate input and re-design.")
            #     logger.info("Assuming a default value of 1.0.")
            #     self.allowable_utilization_ratio = 1.0
            #     self.design_status = False
            #     self.design_status_list.append(self.design_status)

            # if (self.effective_area_factor <= 0.10) or (self.effective_area_factor > 1.0):
            #     logger.warning("The defined value of Effective Area Factor in the design preferences tab is out of the suggested range.")
            #     logger.info("Provide an appropriate input and re-design.")
            #     logger.info("Assuming a default value of 1.0.")
            #     self.effective_area_factor = 1.0
            #     self.design_status = False
            #     self.design_status_list.append(self.design_status)

            # if (self.steel_cost_per_kg == 0.10) or (self.effective_area_factor > 1.0):
            #     logger.warning("The defined value of the cost of steel (in INR) in the design preferences tab is out of the suggested range.")
            #     logger.info("Provide an appropriate input and re-design.")
            #     logger.info("Assuming a default rate of 50 (INR/kg).")
            #     self.steel_cost_per_kg = 50
            #     self.design_status = False
            #     self.design_status_list.append(self.design_status)
            print(f"\n self.input_section_list{self.input_section_list}")
            if len(self.input_section_list) > 0:

                # initializing lists to store the optimum results based on optimum UR and cost

                # 1- Based on optimum UR
                self.optimum_section_ur_results = {}
                self.optimum_section_ur = []

                # 2 - Based on optimum cost
                self.optimum_section_cost_results = {}
                self.optimum_section_cost = []

                i = 1
                for section in self.input_section_list:  # iterating the design over each section to find the most optimum section

                    # fetching the section properties of the selected section
                    if self.sec_profile == VALUES_SEC_PROFILE_Compression_Strut[0]:  # Angles 
                        self.section_property = Angle(designation=section, material_grade=self.material)
                    elif self.sec_profile == VALUES_SEC_PROFILE_Compression_Strut[1]:  # Back to Back Angles 
                        self.section_property = Angle(designation=section, material_grade=self.material)
                    # elif self.sec_profile == VALUES_SEC_PROFILE[2]:  # Channels
                    #     self.section_property = RHS(designation=section, material_grade=self.material)
                    # elif self.sec_profile == VALUES_SEC_PROFILE[3]:  # Columns
                    #     self.section_property = SHS(designation=section, material_grade=self.material)
                    # elif self.sec_profile == VALUES_SEC_PROFILE[4]:  # CHS
                    #     self.section_property = CHS(designation=section, material_grade=self.material)
                    else:   #Why?
                        self.section_property = Column(designation=section, material_grade=self.material)

                    self.material_property.connect_to_database_to_get_fy_fu(self.material, max(self.section_property.flange_thickness, self.section_property.web_thickness))

                    self.epsilon = math.sqrt(250 / self.material_property.fy)

                    print(f"Working correct here")
                    input("?")
                    # initialize lists for updating the results dictionary
                    list_zz = []
                    list_yy = []

                    list_zz.append(section)
                    list_yy.append(section)

                    # Step 1 - computing the effective sectional area
                    self.section_class = self.input_section_classification[section]

                    if self.section_class == 'Slender':
                        logger.warning("The trial section ({}) is Slender. Computing the Effective Sectional Area as per Sec. 9.7.2, "
                                    "Fig. 2 (B & C) of The National Building Code of India (NBC), 2016.".format(section))

                        if (self.sec_profile == VALUES_SEC_PROFILE[0]) or (self.sec_profile == VALUES_SEC_PROFILE[1]):  # Beams or Columns
                            self.effective_area = (2 * ((31.4 * self.epsilon * self.section_property.flange_thickness) *
                                                        self.section_property.flange_thickness)) + \
                                                (2 * ((21 * self.epsilon * self.section_property.web_thickness) * self.section_property.web_thickness))
                        elif (self.sec_profile == VALUES_SEC_PROFILE[2]) or (self.sec_profile == VALUES_SEC_PROFILE[3]):
                            self.effective_area = (2 * 21 * self.epsilon * self.section_property.flange_thickness) * 2
                    else:
                        self.effective_area = self.section_property.area  # mm2
                        # print(f"self.effective_area{self.effective_area}")

                    # reduction of the area based on the connection requirements (input from design preferences)
                    if self.effective_area_factor < 1.0:
                        self.effective_area = round(self.effective_area * self.effective_area_factor, 2)

                        logger.warning("Reducing the effective sectional area as per the definition in the Design Preferences tab.")
                        logger.info("The actual effective area is {} mm2 and the reduced effective area is {} mm2 [Reference: Cl. 7.3.2, IS 800:2007]".
                                    format(round((self.effective_area / self.effective_area_factor), 2), self.effective_area))
                    else:
                        if self.section_class != 'Slender':
                            logger.info("The effective sectional area is taken as 100% of the cross-sectional area [Reference: Cl. 7.3.2, IS 800:2007].")

                    list_zz.append(self.section_class)
                    list_yy.append(self.section_class)

                    list_zz.append(self.effective_area)
                    list_yy.append(self.effective_area)

                    # Step 2 - computing the design compressive stress

                    # 2.1 - Buckling curve classification and Imperfection factor
                    if (self.sec_profile == VALUES_SEC_PROFILE[0]) or (self.sec_profile == VALUES_SEC_PROFILE[1]):  # Beams or Columns

                        if self.section_property.type == 'Rolled':
                            self.buckling_class_zz = IS800_2007.cl_7_1_2_2_buckling_class_of_crosssections(self.section_property.flange_width,
                                                                                                        self.section_property.depth,
                                                                                                        self.section_property.flange_thickness,
                                                                                                        cross_section='Rolled I-sections',
                                                                                                        section_type='Hot rolled')['z-z']
                            self.buckling_class_yy = IS800_2007.cl_7_1_2_2_buckling_class_of_crosssections(self.section_property.flange_width,
                                                                                                        self.section_property.depth,
                                                                                                        self.section_property.flange_thickness,
                                                                                                        cross_section='Rolled I-sections',
                                                                                                        section_type='Hot rolled')['y-y']
                        else:
                            self.buckling_class_zz = IS800_2007.cl_7_1_2_2_buckling_class_of_crosssections(self.section_property.flange_width,
                                                                                                        self.section_property.depth,
                                                                                                        self.section_property.flange_thickness,
                                                                                                        cross_section='Welded I-section',
                                                                                                        section_type='Hot rolled')['z-z']
                            self.buckling_class_yy = IS800_2007.cl_7_1_2_2_buckling_class_of_crosssections(self.section_property.flange_width,
                                                                                                        self.section_property.depth,
                                                                                                        self.section_property.flange_thickness,
                                                                                                        cross_section='Welded I-section',
                                                                                                        section_type='Hot rolled')['y-y']
                    else:
                        self.buckling_class_zz = 'a'
                        self.buckling_class_yy = 'a'

                    self.imperfection_factor_zz = IS800_2007.cl_7_1_2_1_imperfection_factor(buckling_class=self.buckling_class_zz)
                    self.imperfection_factor_yy = IS800_2007.cl_7_1_2_1_imperfection_factor(buckling_class=self.buckling_class_yy)

                    list_zz.append(self.buckling_class_zz)
                    list_yy.append(self.buckling_class_yy)

                    list_zz.append(self.imperfection_factor_zz)
                    list_yy.append(self.imperfection_factor_yy)

                    # 2.2 - Effective length
                    self.effective_length_zz = IS800_2007.cl_7_2_2_effective_length_of_prismatic_compression_members(self.length_zz ,
                                                                                                                    end_1=self.end_1,
                                                                                                                    end_2=self.end_2)  # mm
                    self.effective_length_yy = IS800_2007.cl_7_2_2_effective_length_of_prismatic_compression_members(self.length_yy ,
                                                                                                                    end_1=self.end_1,
                                                                                                                    end_2=self.end_2)  # mm

                    list_zz.append(self.effective_length_zz)
                    list_yy.append(self.effective_length_yy)

                    # 2.3 - Effective slenderness ratio
                    self.effective_sr_zz = self.effective_length_zz / self.section_property.rad_of_gy_z
                    self.effective_sr_yy = self.effective_length_yy / self.section_property.rad_of_gy_y

                    list_zz.append(self.effective_sr_zz)
                    list_yy.append(self.effective_sr_yy)

                    # 2.4 - Euler buckling stress
                    self.euler_bs_zz = (math.pi ** 2 * self.section_property.modulus_of_elasticity) / self.effective_sr_zz ** 2
                    self.euler_bs_yy = (math.pi ** 2 * self.section_property.modulus_of_elasticity) / self.effective_sr_yy ** 2

                    list_zz.append(self.euler_bs_zz)
                    list_yy.append(self.euler_bs_yy)

                    # 2.5 - Non-dimensional effective slenderness ratio
                    self.non_dim_eff_sr_zz = math.sqrt(self.material_property.fy / self.euler_bs_zz)
                    self.non_dim_eff_sr_yy = math.sqrt(self.material_property.fy / self.euler_bs_yy)
                    # print(f"self.non_dim_eff_sr_zz{self.non_dim_eff_sr_yy},self.phi_yy{self.non_dim_eff_sr_yy}/n")

                    list_zz.append(self.non_dim_eff_sr_zz)
                    list_yy.append(self.non_dim_eff_sr_yy)

                    # 2.5 - phi
                    self.phi_zz = 0.5 * (1 + (self.imperfection_factor_zz * (self.non_dim_eff_sr_zz - 0.2)) + self.non_dim_eff_sr_zz ** 2)
                    self.phi_yy = 0.5 * (1 + (self.imperfection_factor_yy * (self.non_dim_eff_sr_yy - 0.2)) + self.non_dim_eff_sr_yy ** 2)
                    # print(f"self.phi_zz{self.phi_zz},self.phi_yy{self.phi_yy}, self.imperfection_factor_zz{self.imperfection_factor_zz}")

                    list_zz.append(self.phi_zz)
                    list_yy.append(self.phi_yy)

                    # 2.6 - Design compressive stress
                    self.stress_reduction_factor_zz = 1 / (self.phi_zz + (self.phi_zz ** 2 - self.non_dim_eff_sr_zz ** 2) ** 0.5)
                    self.stress_reduction_factor_yy = 1 / (self.phi_yy + (self.phi_yy ** 2 - self.non_dim_eff_sr_yy ** 2) ** 0.5)

                    list_zz.append(self.stress_reduction_factor_zz)
                    list_yy.append(self.stress_reduction_factor_yy)

                    self.f_cd_1_zz = (self.stress_reduction_factor_zz * self.material_property.fy) / self.gamma_m0
                    self.f_cd_1_yy = (self.stress_reduction_factor_yy * self.material_property.fy) / self.gamma_m0
                    self.f_cd_2 = self.material_property.fy / self.gamma_m0

                    self.f_cd_zz = min(self.f_cd_1_zz, self.f_cd_2)
                    self.f_cd_yy = min(self.f_cd_1_yy, self.f_cd_2)

                    self.f_cd = min(self.f_cd_zz, self.f_cd_yy)

                    list_zz.append(self.f_cd_1_zz)
                    list_yy.append(self.f_cd_1_yy)

                    list_zz.append(self.f_cd_2)
                    list_yy.append(self.f_cd_2)

                    list_zz.append(self.f_cd_zz)
                    list_yy.append(self.f_cd_yy)

                    list_zz.append(self.f_cd)
                    list_yy.append(self.f_cd)

                    # 2.7 - Capacity of the section
                    self.section_capacity = self.f_cd * self.effective_area  # N

                    list_zz.append(self.section_capacity)
                    list_yy.append(self.section_capacity)

                    # 2.8 - UR
                    self.ur = round(self.load.axial_force / self.section_capacity, 3)

                    list_zz.append(self.ur)
                    list_yy.append(self.ur)
                    self.optimum_section_ur.append(self.ur)

                    # 2.9 - Cost of the section in INR
                    self.cost = (self.section_property.unit_mass * self.section_property.area * 1e-4) * min(self.length_zz, self.length_yy) * \
                                self.steel_cost_per_kg

                    list_zz.append(self.cost)
                    list_yy.append(self.cost)
                    self.optimum_section_cost.append(self.cost)
                    # print(f"list_zz{list_zz},list_yy{list_yy} ")

                    # Step 3 - Storing the optimum results to a list in a descending order

                    list_1 = ['Designation', 'Section class', 'Effective area', 'Buckling_curve_zz', 'IF_zz', 'Effective_length_zz', 'Effective_SR_zz',
                            'EBS_zz', 'ND_ESR_zz', 'phi_zz', 'SRF_zz', 'FCD_1_zz', 'FCD_2', 'FCD_zz', 'FCD', 'Capacity', 'UR', 'Cost', 'Designation',
                            'Section class', 'Effective area', 'Buckling_curve_yy', 'IF_yy', 'Effective_length_yy', 'Effective_SR_yy', 'EBS_yy',
                            'ND_ESR_yy', 'phi_yy', 'SRF_yy', 'FCD_1_yy', 'FCD_2', 'FCD_yy', 'FCD', 'Capacity', 'UR', 'Cost']

                    # 1- Based on optimum UR
                    self.optimum_section_ur_results[self.ur] = {}

                    list_2 = list_zz + list_yy
                    for j in list_1:
                        # k = 0
                        for k in list_2:
                            self.optimum_section_ur_results[self.ur][j] = k
                            # k += 1
                            list_2.pop(0)
                            break

                    # 2- Based on optimum cost
                    self.optimum_section_cost_results[self.cost] = {}

                    list_2 = list_zz + list_yy                                  #Why?
                    for j in list_1:
                        for k in list_2:
                            self.optimum_section_cost_results[self.cost][j] = k
                            list_2.pop(0)
                            break
            else:
                logger.warning("The section(s) defined for performing the column design is/are not selected based on the selected Inputs and/or "
                            "Design Preferences")
                logger.error("Cannot compute!")
                logger.info("Change the inputs provided and re-design.")
                self.design_status = False
                self.design_status_list.append(self.design_status)
                # print(f"design_status_list{self.design_status_list}")

    def results(self):
        """ """
        # sorting results from the dataset

        # results based on UR
        if self.optimization_parameter == 'Utilization Ratio':
            filter_UR = filter(lambda x: x <= min(self.allowable_utilization_ratio, 1.0), self.optimum_section_ur)
            self.optimum_section_ur = list(filter_UR)

            self.optimum_section_ur.sort()
            # print(f"self.optimum_section_ur{self.optimum_section_ur}")
            #print(f"self.result_UR{self.result_UR}")

            # selecting the section with most optimum UR
            if len(self.optimum_section_ur) == 0:  # no design was successful
                logger.warning("The sections selected by the solver from the defined list of sections did not satisfy the Utilization Ratio (UR) "
                                "criteria")
                logger.error("The solver did not find any adequate section from the defined list.")
                logger.info("Re-define the list of sections or check the Design Preferences option and re-design.")
                self.design_status = False
                self.design_status_list.append(self.design_status)

            else:
                self.result_UR = self.optimum_section_ur[-1]  # optimum section which passes the UR check
                print(f"self.result_UR{self.result_UR}")
                self.design_status = True

        else:  # results based on cost
            self.optimum_section_cost.sort()

            # selecting the section with most optimum cost
            self.result_cost = self.optimum_section_cost[0]

        # print results
        if len(self.optimum_section_ur) == 0:
            logger.warning(
                "The sections selected by the solver from the defined list of sections did not satisfy the Utilization Ratio (UR) "
                "criteria")
            logger.error("The solver did not find any adequate section from the defined list.")
            logger.info("Re-define the list of sections or check the Design Preferences option and re-design.")
            self.design_status = False
            self.design_status_list.append(self.design_status)
            pass
        else:
            if self.optimization_parameter == 'Utilization Ratio':
                self.result_designation = self.optimum_section_ur_results[self.result_UR]['Designation']
                self.result_section_class = self.optimum_section_ur_results[self.result_UR]['Section class']
                self.result_effective_area = self.optimum_section_ur_results[self.result_UR]['Effective area']

                self.result_bc_zz = self.optimum_section_ur_results[self.result_UR]['Buckling_curve_zz']
                self.result_bc_yy = self.optimum_section_ur_results[self.result_UR]['Buckling_curve_yy']

                self.result_IF_zz = self.optimum_section_ur_results[self.result_UR]['IF_zz']
                self.result_IF_yy = self.optimum_section_ur_results[self.result_UR]['IF_yy']

                self.result_eff_len_zz = self.optimum_section_ur_results[self.result_UR]['Effective_length_zz']
                self.result_eff_len_yy = self.optimum_section_ur_results[self.result_UR]['Effective_length_yy']

                self.result_eff_sr_zz = self.optimum_section_ur_results[self.result_UR]['Effective_SR_zz']
                self.result_eff_sr_yy = self.optimum_section_ur_results[self.result_UR]['Effective_SR_yy']

                self.result_ebs_zz = self.optimum_section_ur_results[self.result_UR]['EBS_zz']
                self.result_ebs_yy = self.optimum_section_ur_results[self.result_UR]['EBS_yy']

                self.result_nd_esr_zz = self.optimum_section_ur_results[self.result_UR]['ND_ESR_zz']
                self.result_nd_esr_yy = self.optimum_section_ur_results[self.result_UR]['ND_ESR_yy']

                self.result_phi_zz = self.optimum_section_ur_results[self.result_UR]['phi_zz']
                self.result_phi_yy = self.optimum_section_ur_results[self.result_UR]['phi_yy']

                self.result_srf_zz = self.optimum_section_ur_results[self.result_UR]['SRF_zz']
                self.result_srf_yy = self.optimum_section_ur_results[self.result_UR]['SRF_yy']

                self.result_fcd_1_zz = self.optimum_section_ur_results[self.result_UR]['FCD_1_zz']
                self.result_fcd_1_yy = self.optimum_section_ur_results[self.result_UR]['FCD_1_yy']

                self.result_fcd_2 = self.optimum_section_ur_results[self.result_UR]['FCD_2']

                self.result_fcd_zz = self.optimum_section_ur_results[self.result_UR]['FCD_zz']
                self.result_fcd_yy = self.optimum_section_ur_results[self.result_UR]['FCD_yy']

                self.result_fcd = self.optimum_section_ur_results[self.result_UR]['FCD']
                self.result_capacity = self.optimum_section_ur_results[self.result_UR]['Capacity']
                self.result_cost = self.optimum_section_ur_results[self.result_UR]['Cost']
            else:
                self.result_UR = self.optimum_section_cost_results[self.result_cost]['UR']

                # checking if the selected section based on cost satisfies the UR
                if self.result_UR > min(self.allowable_utilization_ratio, 1.0):

                    trial_cost = []
                    for cost in self.optimum_section_cost:
                        self.result_UR = self.optimum_section_cost_results[cost]['UR']
                        if self.result_UR <= min(self.allowable_utilization_ratio, 1.0):
                            trial_cost.append(cost)

                    trial_cost.sort()

                    if len(trial_cost) == 0:  # no design was successful
                        logger.warning("The sections selected by the solver from the defined list of sections did not satisfy the Utilization Ratio (UR) "
                                        "criteria")
                        logger.error("The solver did not find any adequate section from the defined list.")
                        logger.info("Re-define the list of sections or check the Design Preferences option and re-design.")
                        self.design_status = False
                        self.design_status_list.append(self.design_status)
                        print(f"design_status_list{self.design_status} \n")
                    else:
                        self.result_cost = trial_cost[0]  # optimum section based on cost which passes the UR check
                        self.design_status = True

                # results
                self.result_designation = self.optimum_section_cost_results[self.result_cost]['Designation']
                self.result_section_class = self.optimum_section_cost_results[self.result_cost]['Section class']
                self.result_effective_area = self.optimum_section_cost_results[self.result_cost]['Effective area']

                self.result_bc_zz = self.optimum_section_cost_results[self.result_cost]['Buckling_curve_zz']
                self.result_bc_yy = self.optimum_section_cost_results[self.result_cost]['Buckling_curve_yy']

                self.result_IF_zz = self.optimum_section_cost_results[self.result_cost]['IF_zz']
                self.result_IF_yy = self.optimum_section_cost_results[self.result_cost]['IF_yy']

                self.result_eff_len_zz = self.optimum_section_cost_results[self.result_cost]['Effective_length_zz']
                self.result_eff_len_yy = self.optimum_section_cost_results[self.result_cost]['Effective_length_yy']

                self.result_eff_sr_zz = self.optimum_section_cost_results[self.result_cost]['Effective_SR_zz']
                self.result_eff_sr_yy = self.optimum_section_cost_results[self.result_cost]['Effective_SR_yy']

                self.result_ebs_zz = self.optimum_section_cost_results[self.result_cost]['EBS_zz']
                self.result_ebs_yy = self.optimum_section_cost_results[self.result_cost]['EBS_yy']

                self.result_nd_esr_zz = self.optimum_section_cost_results[self.result_cost]['ND_ESR_zz']
                self.result_nd_esr_yy = self.optimum_section_cost_results[self.result_cost]['ND_ESR_yy']

                self.result_phi_zz = self.optimum_section_cost_results[self.result_cost]['phi_zz']
                self.result_phi_yy = self.optimum_section_cost_results[self.result_cost]['phi_yy']

                self.result_srf_zz = self.optimum_section_cost_results[self.result_cost]['SRF_zz']
                self.result_srf_yy = self.optimum_section_cost_results[self.result_cost]['SRF_yy']

                self.result_fcd_1_zz = self.optimum_section_cost_results[self.result_cost]['FCD_1_zz']
                self.result_fcd_1_yy = self.optimum_section_cost_results[self.result_cost]['FCD_1_yy']

                self.result_fcd_2 = self.optimum_section_cost_results[self.result_cost]['FCD_2']

                self.result_fcd_zz = self.optimum_section_cost_results[self.result_cost]['FCD_zz']
                self.result_fcd_yy = self.optimum_section_cost_results[self.result_cost]['FCD_yy']

                self.result_fcd = self.optimum_section_cost_results[self.result_cost]['FCD']
                self.result_capacity = self.optimum_section_cost_results[self.result_cost]['Capacity']

                print(f"design_status_list2{self.design_status}")

        # end of the design simulation
        # overall design status
        for status in self.design_status_list:
            if status is False:
                self.design_status = False
                break
            else:
                self.design_status = True

        if self.design_status:
            logger.info(": ========== Design Status ============")
            logger.info(": Overall Column design is SAFE")
            logger.info(": ========== End Of Design ============")
        else:
            logger.info(": ========== Design Status ============")
            logger.info(": Overall Column design is UNSAFE")
            logger.info(": ========== End Of Design ============")

    ### start writing save_design from here!
    def save_design(self, popup_summary):

        if self.connectivity == 'Hollow/Tubular Column Base':
            if self.dp_column_designation[1:4] == 'SHS':
                select_section_img = 'SHS'
            elif self.dp_column_designation[1:4] == 'RHS':
                select_section_img = 'RHS'
            else:
                select_section_img = 'CHS'
        else:
            if self.column_properties.flange_slope != 90:
                select_section_img = "Slope_Beam"
            else:
                select_section_img = "Parallel_Beam"

            # column section properties
        if self.connectivity == 'Hollow/Tubular Column Base':
            if self.dp_column_designation[1:4] == 'SHS':
                section_type = 'Square Hollow Section (SHS)'
            elif self.dp_column_designation[1:4] == 'RHS':
                section_type = 'Rectangular Hollow Section (RHS)'
            else:
                section_type = 'Circular Hollow Section (CHS)'
        else:
            section_type = 'I Section'


        if self.section_property=='Columns' or self.section_property=='Beams':
            self.report_column = {KEY_DISP_SEC_PROFILE: "ISection",
                                    KEY_DISP_COLSEC_REPORT: self.section_property.designation,
                                    KEY_DISP_MATERIAL: self.section_property.material,
    #                                 KEY_DISP_APPLIED_AXIAL_FORCE: self.section_property.,
                                    KEY_REPORT_MASS: self.section_property.mass,
                                    KEY_REPORT_AREA: round(self.section_property.area * 1e-2, 2),
                                    KEY_REPORT_DEPTH: self.section_property.depth,
                                    KEY_REPORT_WIDTH: self.section_property.flange_width,
                                    KEY_REPORT_WEB_THK: self.section_property.web_thickness,
                                    KEY_REPORT_FLANGE_THK: self.section_property.flange_thickness,
                                    KEY_DISP_FLANGE_S_REPORT: self.section_property.flange_slope,
                                    KEY_REPORT_R1: self.section_property.root_radius,
                                    KEY_REPORT_R2: self.section_property.toe_radius,
                                    KEY_REPORT_IZ: round(self.section_property.mom_inertia_z * 1e-4, 2),
                                    KEY_REPORT_IY: round(self.section_property.mom_inertia_y * 1e-4, 2),
                                    KEY_REPORT_RZ: round(self.section_property.rad_of_gy_z * 1e-1, 2),
                                    KEY_REPORT_RY: round(self.section_property.rad_of_gy_y * 1e-1, 2),
                                    KEY_REPORT_ZEZ: round(self.section_property.elast_sec_mod_z * 1e-3, 2),
                                    KEY_REPORT_ZEY: round(self.section_property.elast_sec_mod_y * 1e-3, 2),
                                    KEY_REPORT_ZPZ: round(self.section_property.plast_sec_mod_z * 1e-3, 2),
                                    KEY_REPORT_ZPY: round(self.section_property.plast_sec_mod_y * 1e-3, 2)}
        else:
            self.report_column = {KEY_DISP_COLSEC_REPORT: self.section_property.designation,
                                    KEY_DISP_MATERIAL: self.section_property.material,
                                    #                                 KEY_DISP_APPLIED_AXIAL_FORCE: self.section_property.,
                                    KEY_REPORT_MASS: self.section_property.mass,
                                    KEY_REPORT_AREA: round(self.section_property.area * 1e-2, 2),
                                    KEY_REPORT_DEPTH: self.section_property.depth,
                                    KEY_REPORT_WIDTH: self.section_property.flange_width,
                                    KEY_REPORT_WEB_THK: self.section_property.web_thickness,
                                    KEY_REPORT_FLANGE_THK: self.section_property.flange_thickness,
                                    KEY_DISP_FLANGE_S_REPORT: self.section_property.flange_slope}


        self.report_input = \
            {KEY_MAIN_MODULE: self.mainmodule,
                KEY_MODULE: self.module, #"Axial load on column "
                KEY_DISP_SECTION_PROFILE: self.sec_profile,
                KEY_MATERIAL: self.material,
                KEY_DISP_ACTUAL_LEN_ZZ: self.length_zz,
                KEY_DISP_ACTUAL_LEN_YY: self.length_yy,
                KEY_DISP_END1: self.end_1,
                KEY_DISP_END2: self.end_2,
                KEY_DISP_AXIAL: self.load,
                KEY_DISP_SEC_PROFILE: self.sec_profile,
                KEY_DISP_SECSIZE: self.result_section_class,
                KEY_DISP_ULTIMATE_STRENGTH_REPORT: self.euler_bs_yy,
                KEY_DISP_YIELD_STRENGTH_REPORT: self.result_bc_yy,


                "Column Section - Mechanical Properties": "TITLE",
                "Section Details": self.report_column,
                }

        self.report_check = []

        self.h = (self.beam_D - (2 * self.beam_tf))

        #1.1 Input sections display
        t1 = ('SubSection', 'List of Input Sections',self.input_section_list),
        self.report_check.append(t1)

        # 2.2 CHECK: Buckling Class - Compatibility Check
        t1 = ('SubSection', 'Buckling Class - Compatibility Check', '|p{4cm}|p{3.5cm}|p{6.5cm}|p{2cm}|')
        self.report_check.append(t1)

        t1 = ("h/bf , tf ", comp_column_class_section_check_required(self.bucklingclass, self.h, self.bf),
                comp_column_class_section_check_provided(self.bucklingclass, self.h, self.bf, self.tf, self.var_h_bf),
                'Compatible')  # if self.bc_compatibility_status is True else 'Not compatible')
        self.report_check.append(t1)

        # 2.3 CHECK: Cross-section classification
        t1 = ('SubSection', 'Cross-section classification', '|p{4.5cm}|p{3cm}|p{6.5cm}|p{1.5cm}|')
        self.report_check.append(t1)

        t1 = ("b/tf and d/tw ", cross_section_classification_required(self.section),
                cross_section_classification_provided(self.tf, self.b1, self.epsilon, self.section, self.b1_tf,
                                                    self.d1_tw, self.ep1, self.ep2, self.ep3, self.ep4),
                'b = bf / 2,d = h – 2 ( T + R1),έ = (250 / Fy )^0.5,Compatible')  # if self.bc_compatibility_status is True else 'Not compatible')
        self.report_check.append(t1)

        # 2.4 CHECK : Member Check
        t1 = ("Slenderness", cl_7_2_2_slenderness_required(self.KL, self.ry, self.lamba),
                cl_7_2_2_slenderness_provided(self.KL, self.ry, self.lamba), 'PASS')
        self.report_check.append(t1)

        t1 = (
        "Design Compressive stress (fcd)", cl_7_1_2_1_fcd_check_required(self.gamma_mo, self.f_y, self.f_y_gamma_mo),
        cl_7_1_2_1_fcd_check_provided(self.facd), 'PASS')
        self.report_check.append(t1)

        t1 = ("Design Compressive strength (Pd)", cl_7_1_2_design_comp_strength_required(self.axial),
                cl_7_1_2_design_comp_strength_provided(self.Aeff, self.facd, self.A_eff_facd), "PASS")
        self.report_check.append(t1)

        t1 = ('', '', '', '')
        self.report_check.append(t1)
        print(sys.path[0])
        rel_path = str(sys.path[0])
        rel_path = rel_path.replace("\\", "/")
        fname_no_ext = popup_summary['filename']
        CreateLatex.save_latex(CreateLatex(), self.report_input, self.report_check, popup_summary, fname_no_ext,
                                rel_path, module=self.module)

