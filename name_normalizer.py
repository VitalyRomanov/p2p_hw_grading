import editdistance

class NNorm:
    '''
    Normalizar for student names
    name_list : list of students' names. Should have first name and last name.
                Deviations cause error
    email_list : parallel list of emails

    performs permutation of first name and last name
    compares given name with the list of permutations
    '''

    def __init__(self,name_list,email_list = None):
        self.names = dict().fromkeys(name_list)
        self.emails = None
        self.inv_emails = None
        if email_list != None:
            self.emails = dict(zip(name_list,email_list))
            self.inv_emails = dict(zip(email_list,name_list))
        for name in self.names:
            fn,ln = name.split(" ")
            self.names[name] = [name, ln+" "+fn]

    def get_info(self,s_name):
        min_name = ""
        min_dist = editdistance.eval(min_name,s_name)
        for name,variations in self.names.items():
            for var in variations:
                dist = editdistance.eval(s_name,var)
                if dist < min_dist:
                    min_dist = dist
                    min_name = name
        email = None
        if self.emails != None:
            email = self.emails[min_name]
        return min_name,email

    def get_name_by_email(self,s_email):
        if self.inv_emails == None:
            raise Exception("Emails were not provided")
        min_email = ""
        min_dist = editdistance.eval(min_email,s_email)
        for email in self.inv_emails:
            dist = editdistance.eval(email,s_email)
            if dist < min_dist:
                min_dist = dist
                min_email = email
        return self.inv_emails[min_email]
