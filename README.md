# Extraction_Automation

This project primarily involves extracting questions, answers, topic names, and test names. It then converts each question into a PDF file and an SVG image. The details of the question are incorporated into the file names. The purpose of developing this project is to build a question pool for an online study platform.


## How to Execute
#### Ubuntu:

- It is recommended to run the code within a virtual environment due to easy usage.
- The project was developed using Python 3.8.10; compatibility issues are unlikely.

1. Install [inkscape AppImage](https://inkscape.org/release/all/gnulinux/appimage/). Version 1.2.2 is recommended.

2. Install these packages.
    ```
    $ apt install tesseract-ocr libtesseract-dev libleptonica-dev pkg-config
    $ apt install tesseract-ocr-tur
    $ apt install pdf2svg 
    ```

3. Edit bashrc file. Add the line below to bashrc.
    ```
    export TESSDATA_PREFIX=/usr/share/tesseract-ocr/4.00/tessdata
    ```
    ```
    $ gedit ~/.bashrc
    ```

4. Clone the Repository

5. Create a Virtual Environment
    ```
    $ cd <PathToRepo>/Extraction_Automation/
    $ python -m venv .venv
    ```

6. Activate the Environment
    ```
    $ source .venv/bin/activate
    ```

7. Install Dependencies
    ```
    $ pip install -r requirements.txt
    ```

8. Configure the `PATH` variable at the end of each code.

9. Execute the Following Command
    ```
    $ python main.py
    $ python main_math.py
    ```

## Example Outputs

#### PDFs:
[Biyoloji-6-Enzimler - 2-5-B.pdf](https://github.com/Alperenlcr/QR_and_Symbol_Detection/files/12402423/Biyoloji-6-Enzimler.-.2-5-B.pdf)

[Matematik-34-Geometrik Cisimler - 2-11-C.pdf](https://github.com/Alperenlcr/QR_and_Symbol_Detection/files/12402424/Matematik-34-Geometrik.Cisimler.-.2-11-C.pdf)

#### SVGs:
![Biyoloji-6-Enzimler - 2-5-B](https://github.com/Alperenlcr/QR_and_Symbol_Detection/assets/75525649/098b6227-0c1b-459b-8b60-fa83e1c31c99)

![Matematik-34-Geometrik Cisimler - 2-11-C](https://github.com/Alperenlcr/QR_and_Symbol_Detection/assets/75525649/46f0ac85-e438-4394-b9b9-17a581aacaca)
