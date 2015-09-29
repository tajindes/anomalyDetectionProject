import java.util.Random;
import java.io.FileWriter;
import java.io.IOException;
import java.sql.Timestamp;
import java.util.Date;
import java.text.DateFormat;
import java.text.Format;
import java.text.SimpleDateFormat;

public class generateUserData {

    public static long beginTime = Timestamp.valueOf("2010-01-01 00:00:00").getTime();
    public static long endTime = Timestamp.valueOf("2015-09-24 00:00:00").getTime();
    public static long diff = endTime - beginTime + 1;              
    public static FileWriter writer = null;
    /**
     * Returns a pseudo-random number between min and max, inclusive.
     * The difference between min and max can be at most
     * <code>Integer.MAX_VALUE - 1</code>.
     *
     * @param min Minimum value
     * @param max Maximum value.  Must be greater than min.
     * @return Integer between min and max, inclusive.
     * @see java.util.Random#nextInt(int)
     */
    public static int randInt(int min, int max) {

        // NOTE: This will (intentionally) not run as written so that folks
        // copy-pasting have to think about how to initialize their
        // Random instance.  Initialization of the Random instance is outside
        // the main scope of the question, but some decent options are to have
        // a field that is initialized once and then re-used as needed or to
        // use ThreadLocalRandom (if using at least Java 1.7).
        Random rand = new Random();

        // nextInt is normally exclusive of the top value,
        // so add 1 to make it inclusive
        int randomNum = rand.nextInt((max - min) + 1) + min;

        return randomNum;
    }

    private static void generateCsvFile(String sFileName)
    {
    //Date Rptd,DR NO,DATE OCC,TIME OCC,AREA,AREA NAME,RD,Crm Cd,Crm Cd Desc,Status,Status Desc,LOCATION,Cross Street,Location 1,crimeType
        try
        {
            writer = new FileWriter(sFileName);
             
            writer.append("DATE_Rptd");
            writer.append(',');
            writer.append("CRIME_Rptd");
            writer.append(',');
            writer.append("DATE_OCC");
            writer.append(',');
            writer.append("TIME_OCC");
            writer.append(',');
            writer.append("AREA");
            writer.append(',');
            writer.append("AREA_NAME");
            writer.append(',');
            writer.append("RD");
            writer.append(',');
            writer.append("Crm_Cd");
            writer.append(',');
            writer.append("Crd_Cd_Desc");
            writer.append(',');
            writer.append("Status");
            writer.append(',');
            writer.append("Status_Desc");
            writer.append(',');
            writer.append("LOCATION");
            writer.append(',');
            writer.append("Cross_Street");
            writer.append(',');
            writer.append("Location_1");
            writer.append(',');
            writer.append("crimeType");
             writer.append('\n');

            //generate whatever data you want
                
            writer.flush();
            //writer.close();
        }
        catch(IOException e)
        {
             e.printStackTrace();
        } 
    }

    public static String getLocation(double x0, double y0, int radius) {
        Random random = new Random();

        // Convert radius from meters to degrees
        double radiusInDegrees = radius / 111000f;

        double u = random.nextDouble();
        double v = random.nextDouble();
        double w = radiusInDegrees * Math.sqrt(u);
        double t = 2 * Math.PI * v;
        double x = w * Math.cos(t);
        double y = w * Math.sin(t);

        // Adjust the x-coordinate for the shrinking of the east-west distances
        double new_x = x / Math.cos(y0);

        /*int dayValue = randInt(1,28); 
        int monthValue = randInt(1,11);
        int yearValue = randInt(2011,2015);
*/
        double foundLongitude = new_x + x0;
        double foundLatitude = y + y0;
        return foundLongitude+","+foundLatitude;
        //System.out.println("Longitude: " + foundLongitude + "  Latitude: " + foundLatitude );
    }

    public static void writeUserData(String sFileName, String numberOfRecords_str) {

        String[] area_name_array = {"central", "south", "east", "west", "north"};        
        String[] crimeTypeArray = {"Robbery","Robbery","Battery","Burglary","Criminal Threats","Vandalism","Traffic Dr","Vehicle Stolen","Abusement","Abusement"};
        int numberOfRecords = Integer.parseInt(numberOfRecords_str);
        
        try
        {
            //FileWriter writer = new FileWriter(sFileName);

            for (int count=0;count<numberOfRecords;count++){                 

                //String location1_random = getLocation(34.114351, -118.357488, 100000);
		String location1_random = getLocation(41.034909, -100.505527, 2200000);
		long date_rptd_random_ts = beginTime + (long) (Math.random() * diff);
                Date date_rptd_random = new Date(date_rptd_random_ts);
                //Date date_occ_random = new Date(beginTime + (long) (Math.random() * diff));

		long tempValue = randInt(100000,129600000);
		Date date_occ_random = new Date(date_rptd_random_ts - tempValue);
		
                //String dr_no_random = ""+ randInt(140000000, 149999999);
                String time_occ_random = "" + randInt(1,23) + "" + randInt(10,59);
		int timeDiffTemp = Integer.parseInt(time_occ_random);
	        String time_reported_random = ""+ randInt(timeDiffTemp,2359);  // 2359 ==> 23:50 ==> 11:59 PM
	        String area_random = ""+randInt(1,250);
                String area_name_random = area_name_array[randInt(0,4)];
                String rd_random = ""+randInt(1,500);
                String crm_cd = "" + randInt(1,1000);
                String crm_cd_value = "CRIMINAL THREATS - NO WEAPON DISPLAY";
                String status = "IC";
                String status_desc = "Invest Cont";
                String location = "olympic blvd";
                String cross_street = "benton way";
                String crimeType_random = crimeTypeArray[randInt(0,9)];
		/*
                while(date_rptd_random.before(date_occ_random)) {
                    date_rptd_random = new Date(beginTime + (long) (Math.random() * diff));
                    date_occ_random = new Date(beginTime + (long) (Math.random() * diff));
                }
		*/

                DateFormat df = new SimpleDateFormat("MM/dd/yyyy");


                Format formatter = new SimpleDateFormat("MM/dd/yyyy");
                String date_rptd_random_str = formatter.format(date_rptd_random);
                String date_occ_random_str = formatter.format(date_occ_random);
                //System.out.println("date_rptd_random is: " + date_rptd_random_str);
                writer.append(date_rptd_random_str);
                writer.append(',');
                writer.append(time_reported_random);
                writer.append(',');
                writer.append(date_occ_random_str);
                writer.append(',');
                writer.append(time_occ_random);
                writer.append(',');
                writer.append(area_random);
                writer.append(',');
                writer.append(area_name_random);
                writer.append(',');
                writer.append(rd_random);
                writer.append(',');
                writer.append(crm_cd);
                writer.append(',');
                writer.append(crm_cd_value);
                writer.append(',');
                writer.append(status);
                writer.append(',');
                writer.append(status_desc);
                writer.append(',');
                writer.append(location);
                writer.append(',');
                writer.append(cross_street);
                writer.append(',');
                writer.append(location1_random);
                writer.append(',');
                writer.append(crimeType_random);

                writer.append('\n');
        
                writer.flush();
            
                //generate whatever data you want
            }
            writer.close();
        
        }
        catch(IOException e)
        {
             e.printStackTrace();
        } 
    }
    public static void main(String args[]) {

        generateCsvFile(args[0]); 

        //getLocation(34.114351, -118.357488, 500);
        writeUserData(args[0], args[1]);
    }
}
