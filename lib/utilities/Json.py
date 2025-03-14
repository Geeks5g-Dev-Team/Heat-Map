import json


class Json ():

    def create_json_from_array(self, data, filename="output.json", indent=4):
        """
        Creates a JSON file from an array of data.

        Parameters:
        data (list): The array data to convert to JSON
        filename (str): The name of the output file (default: "output.json")
        indent (int): Number of spaces for indentation in the JSON file (default: 4)

        Returns:
        bool: True if successful, False otherwise
        """
        try:
            # Write the data to a JSON file
            with open(filename, 'w') as json_file:
                json.dump(data, json_file, indent=indent)

            print(f"JSON file '{filename}' created successfully.")
            return True

        except Exception as e:
            print(f"Error creating JSON file: {str(e)}")
            return False
