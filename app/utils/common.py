

class JsonResponse(object):

    def from_json(cls, json_data):
        for key in json_data:
            if key in cls.READONLY_FIELDS:
                raise ValueError("Field '%s' is read only" % key)
            elif key in cls.REQUIRED_FIELDS and\
                            json_data.get(key) is None and\
                    not getattr(cls, key):
                raise ValueError("Field '%s' is required")
            setattr(cls, key, json_data.get(key))
        return cls


class GenerateData(object):

    def __init__(self, model, db, csv_file):
        self.model = model
        self.db = db
        self.csv_file = csv_file

    @staticmethod
    def _auto_parse_val(val):
        try:
            if '.' in val:
                val = float(val)
            else:
                raise Exception
        except:
            try:
                val = int(val)
            except:
                if hasattr(val, 'lower') and val.lower() == "true":
                    val = True
                elif hasattr(val, 'lower') and val.lower() == "false":
                    val = False
        return val

    def generate_fake_data(self):
        with open(self.csv_file) as fh:

            lines = fh.read().split('\n')
            if not [line for line in lines if line]:
                return

            keys = lines[0].split(',')
            if not [key for key in keys if key]:
                return

            for line in lines[1:]:
                model_obj = self.model()
                values = line.split(',')
                for index in range(len(keys)):
                    setattr(model_obj, keys[index], values[index])

                self.db.session.add(model_obj)
            print("%s data fields added to '%s'" % (len(lines[1:]), self.model))
            self.db.session.commit()
