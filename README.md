# **LM Studio Chat Interface**

A user-friendly chat interface for LM Studio that allows you to upload and reference text documents in your conversations with AI models. This application provides a simple way to interact with your locally running LM Studio instance and analyze text documents.

## **✨ Features**

- **Easy File Upload**: Upload .txt files through a simple interface
- **Intuitive File Referencing**: Use @mentions to reference files (e.g., @document.txt)
- **Dynamic Model Selection**: Automatically uses available models from your LM Studio instance
- **Configurable Connection**: Easily set IP address and port for LM Studio connection
- **Real-time File List**: See all available documents with one-click reference copying
- **Responsive Design**: Works well on both desktop and mobile devices

## **🚀 Quick Start**

### **Prerequisites**

- Python 3.x
- LM Studio installed and running
- Modern web browser

### **Installation**

1. **Clone or download the repository**

2. **Set up a virtual environment:**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment:**
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install required packages:**
   ```bash
   pip install -r requirements.txt
   ```

### **Running the Application**

1. **Start LM Studio** and load your preferred model

2. **Run the Flask application:**
   ```bash
   python app.py
   ```

3. **Access the interface** at http://localhost:5000

## **📝 Usage Guide**

### **Uploading Documents**
1. Click the file input in the "Upload Text Documents" section
2. Select a .txt file
3. Click "Upload"

### **Referencing Documents in Chat**
There are two ways to reference documents:

1. **Direct @mention:**
   ```
   What's in @document.txt?
   ```

2. **Copy Reference:**
   - Click "Copy Reference" next to any file in the list
   - Paste into your message

### **Configuring LM Studio Connection**
1. Enter the IP address (default: localhost)
2. Enter the port number (default: 1234)
3. Click "Save Configuration"

## **🔍 Example Queries**

- ```What's in @test.txt?```
- ```Can you analyze @document.txt for key points?```
- ```Summarize @report.txt in bullet points```
- ```Compare the contents of @file1.txt and @file2.txt```

## **🛠️ Technical Details**

- Built with Flask and modern JavaScript
- Uses LM Studio's API for model interaction
- Automatic model detection and selection
- Real-time file list updates
- Error handling and debugging capabilities

## **💡 Tips**

1. Make sure LM Studio is running before starting the chat
2. Keep text files relatively small for best performance
3. Use clear, specific questions when referencing files
4. Check the copied @mentions in your message before sending

## **🔧 Troubleshooting**

If you encounter issues:

1. **Can't connect to LM Studio:**
   - Verify LM Studio is running
   - Check IP address and port configuration
   - Ensure no firewall blocking

2. **File not found:**
   - Confirm file was uploaded successfully
   - Check file name spelling in @mention
   - Verify file exists in uploads folder

3. **No response:**
   - Check LM Studio console for errors
   - Verify model is loaded in LM Studio
   - Check network connection

## **🤝 Contributing**

Feel free to:
- Submit bug reports
- Propose new features
- Submit pull requests

## **📜 License**

This project is for educational purposes.

## **👏 Acknowledgments**

- Thanks to the LM Studio team
- All contributors and users

---

**Note:** This interface is designed to work with LM Studio's API. Make sure you're using a compatible version of LM Studio.