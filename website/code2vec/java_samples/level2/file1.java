
String x (String filename){
    File file = new File(filename);

    
    String fileName = file.toString();

    
    int index = fileName.lastIndexOf('.');

    
    if(index>0){
        String extension = fileName.substring(index + 1);
    }
}