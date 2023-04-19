
String x (String filename){
    File file = new File(filename);

    //convert the filename into string
    String fileName = file.toString();

    //look for start of the extension, marked by a period
    int index = fileName.lastIndexOf('.');

    //if there is an extiension, store it in vairable extention
    if(index>0){
        String extension = fileName.substring(index + 1);
    }
}