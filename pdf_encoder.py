import base64
import os

"""
Base64 Encorder/Decorder for PDF
Author: Madumal Jeewantha
Version: Python 3.7
"""


class PDFtoBase64:

    encoded_data_dir = os.path.join(os.getcwd(), "encoded_data")
    decoded_data_dir = os.path.join(os.getcwd(), "decoded_data")
    copy_to_clipboard = False

    def __init__(self):
        pass

    def check_decode_dir(self):
        """
        Check encoded_data directory
        """
        if not os.path.isdir(self.encoded_data_dir):
            os.mkdir(self.encoded_data_dir)
            print("Created directory: ", self.encoded_data_dir)

    def check_encode_dir(self):
        """
        Check decoded_data directory
        """
        if not os.path.isdir(self.decoded_data_dir):
            os.mkdir(self.decoded_data_dir)
            print("Created directory: ", self.decoded_data_dir)

    def encorder(self):
        """
        Encode to Base64 and save as text files
        """
        self.check_decode_dir()

        files = self.get_files(".pdf")
        for item in files:

            # open binary file in read mode
            with open(item['filePath'], "rb") as pdf:
                pdf_data = pdf.read()
                print("Encoding in progress: ", item['filePath'])
                encoded_pdf_data = base64.encodebytes(pdf_data)

            file_name = os.path.join(
                self.encoded_data_dir, item['fileName'] + ".txt")

            with open(file_name, "wb") as encoded_data:
                encoded_data.write(encoded_pdf_data)

            if self.copy_to_clipboard:

                with open(file_name, "r") as encoded_data:
                    # self.add_to_clipboard(encoded_data.read())
                    clipboard.copy(encoded_data.read())

                print("Encoded content copied to clipboard: ",
                      item['fileName'])
                while True:
                    next = input(
                        "Press (Y) to confirm and encode next file:").lower()
                    if next == 'y':
                        break

    def decorder(self):
        """
        Decode to PDF files
        """
        self.check_encode_dir()

        files = self.get_files(".txt")
        for item in files:

            # open binary file in read mode
            with open(item['filePath'], "rb") as pdf:
                pdf_data = pdf.read()
                print("Decoding in progress: ", item['filePath'])
                decoded_pdf_data = base64.decodebytes(pdf_data)

            file_name = os.path.join(
                self.decoded_data_dir, item['fileName'] + ".pdf")

            with open(file_name, "wb") as decoded_data:
                decoded_data.write(decoded_pdf_data)

    def get_files(self, extension):
        """
        Get PDF file full path in current directory as a list
        """
        files = []

        cwd = os.getcwd()
        basepath = cwd

        for entry in os.listdir(basepath):
            if os.path.isfile(os.path.join(basepath, entry)):

                # Check file extension
                if entry.endswith(extension):
                    print("Valid file found: ", entry)
                    data = {
                        'fileName': os.path.splitext(entry)[0],
                        'filePath': os.path.join(cwd, entry)
                    }
                    files.append(data)
                else:
                    print("Invalid file found: ", entry)

        return files


if __name__ == '__main__':
    print("Welcome to PDF Base64 encorder.")
    print("1 : Encorder")
    print("2 : Decorder")

    method = input("Choose a method (1 or 2):")
    converter = PDFtoBase64()

    if method == "1":
        try:
            import clipboard
        except ImportError:
            print(
                "Warning: If you want to use clipboard feature, please install clipboard: pip install clipboard")
        else:
            clipboard_option = input(
                "Do you want to enable copy to clipboard option (Y/n):").lower()
            if clipboard_option == 'y':
                converter.copy_to_clipboard = True
            else:
                converter.copy_to_clipboard = False
        converter.encorder()

    elif method == "2":
        converter.decorder()
    else:
        print("Wrong input.")
