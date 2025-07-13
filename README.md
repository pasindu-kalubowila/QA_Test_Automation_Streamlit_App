# 🤖 QE Test Automation Suite

**Enterprise-Grade Test Case Generator & Selenium Automation Code Builder (Powered by Gemini 1.5 Flash & Streamlit)**

---

## Overview

The QE Test Automation Suite is an all-in-one platform for quality engineers to:

- ✨ **Generate professional test cases** from requirements or user stories using AI
- 🧑‍💻 **Produce production-ready Java Selenium automation code** (TestNG, Page Object Model, Allure, Log4j2, etc.)
- 🏗️ **Build complete automation frameworks** adhering to enterprise standards
- 📄 **Manage, edit, and download** test cases and automation artifacts in a user-friendly Streamlit interface

This app leverages Google's Gemini 1.5 Flash model, providing industry-leading test design and code generation capabilities.

---

## 🚀 Features

- **AI-Powered Test Case Generation:**  
  Input requirements or user stories, and instantly generate comprehensive test cases in JSON format.

- **Manual Test Case Authoring:**  
  Create, edit, and manage your own test cases with rich forms and attachment support.

- **Bulk Test Case Management:**  
  Select, copy, delete, and batch-generate automation code for multiple test cases.

- **Automation Code Generation:**  
  Generate Java Selenium automation code (TestNG, POM, Allure, Log4j2, explicit waits, thread safety, etc.) for:
  - Individual test cases
  - Combined test suite (multiple test cases in one suite)

- **Downloadable Artifacts:**  
  Download generated code as a ready-to-use ZIP archive.

- **Enterprise UI/UX:**  
  Modern, responsive Streamlit web app with advanced CSS styling and usability features.

---

## 🏗️ Tech Stack

- [Streamlit](https://streamlit.io/) — UI framework
- [Google Gemini 1.5 Flash](https://ai.google.dev/) — AI test case/code generation
- [PyPDF2](https://pypi.org/project/pypdf2/), [python-docx](https://pypi.org/project/python-docx/), [pandas](https://pandas.pydata.org/) — File parsing
- [Base64](https://docs.python.org/3/library/base64.html) — Attachment encoding

---

## ⚡ Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/pasindu-kalubowila/QA_Test_Automation_Streamlit_App.git
cd QA_Test_Automation_Streamlit_App
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Up Environment Variables

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

> **Note:** You need access to [Google Gemini API](https://makersuite.google.com/app/apikey).

### 4. Run the App

```bash
streamlit run app.py
```

---

## 🧪 Usage

### Home

- Welcome & feature summary
- Navigation sidebar

### Test Case Generator

- **Manual Creation:**  
  Fill in scenario, steps, expected results, and attach files/screenshots.
- **AI Generation:**  
  Enter user stories or requirements → Get instant, structured test cases.
- **Bulk Actions:**  
  Select, copy, delete, or send test cases to automation.

### Test Automation

- **Combined Suite:**  
  Generate a single Java test class for multiple selected test cases.
- **Separate Files:**  
  Generate separate Java classes per test case.
- **Download ZIP:**  
  Download all Java source files as a ready-to-import zip.

---

## 🛡️ Enterprise Java Standards

- Java 17
- Selenium WebDriver
- TestNG
- Page Object Model (with `@FindBy`)
- WebDriver Factory (Factory Pattern)
- Singleton configuration
- Log4j2 logging
- Allure reporting
- Explicit waits with `WebDriverWait`
- Thread-safe implementation
- Meaningful assertions

---

## 📂 File Upload Support

- **Test Case Attachments:**  
  - Images: PNG, JPG, JPEG
  - Docs: PDF, TXT
- **Requirement Uploads:**  
  - TXT, PDF, DOCX, CSV, XLSX (auto-parsed)

---

## ✨ Screenshots

<p align="center">
  <img width="1919" height="990" alt="home_page" src="https://github.com/user-attachments/assets/39ff951b-2890-4ea1-8274-7ef85ab1bd48" />
</p>

<p align="center">
  <img width="1918" height="993" alt="test_case_generate_page" src="https://github.com/user-attachments/assets/2ff025d5-8acb-4e53-a944-a8ae8535bf41" />
</p>

<p align="center">
  <img width="1918" height="995" alt="test_automation_page" src="https://github.com/user-attachments/assets/29490b51-ac83-403a-bd9d-38dd1a2caf4f" />
</p>

<p align="center">
  <img width="1916" height="946" alt="generate_test_case_from_requirement" src="https://github.com/user-attachments/assets/344ed5f8-b66e-476e-9c84-fd81a105ae33" />
</p>

---

## 📝 Requirements

See [`requirements.txt`](./requirements.txt):

- `streamlit`
- `python-dotenv`
- `google-generativeai`
- `PyPDF2`
- `python-docx`
- `pandas`
- `openpyxl`

---

## 🙌 Contributing

Pull requests are welcome!  
For major changes, please open an issue first to discuss what you would like to change.

---

## 📄 License

[MIT](LICENSE)

---

## 👤 Author

- [Pasindu Kalubowila](https://github.com/pasindu-kalubowila)

---

> QE Test Automation Suite | Powered by Gemini 1.5 Flash & Streamlit
