class FormErrorMixin(object):
    def get_error(self):
        """
        get error list
        :return: errors
        """
        errors = []
        for fieldName, errorMessages in self.errors.items():
            errData = {fieldName: []}
            for error in errorMessages:
                errData[fieldName].append(error)
            errors.append(errData)
        return errors
