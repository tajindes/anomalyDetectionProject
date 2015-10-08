import java.util.Random;
import java.io.FileWriter;
import java.io.IOException;
import java.sql.Timestamp;
import java.util.Date;
import java.text.DateFormat;
import java.text.Format;
import java.text.SimpleDateFormat;

public class generateUserData_RT {

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
             
            writer.append("userID");
            writer.append(',');
      	    writer.append("userName");
            writer.append(',');
            writer.append("latitude");
            writer.append(',');
            writer.append("longitude");
            writer.append(',');
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

        //String[] area_name_array = {"central", "south", "east", "west", "north"};        
        String[] userNameArray = {"Robert","Tajinder","John","Patrick","Ronak","Austin","Insight","HackLock","Andy","Nehal"};
        int numberOfRecords = Integer.parseInt(numberOfRecords_str);
        
        try
        {
            //FileWriter writer = new FileWriter(sFileName);

            for (int count=0;count<numberOfRecords;count++){                 

                String location1_random = getLocation(34.114351, -118.357488, 100000);
		//String location1_random = getLocation(41.034909, -100.505527, 2200000);
		//long date_rptd_random_ts = beginTime + (long) (Math.random() * diff);
                //Date date_rptd_random = new Date(date_rptd_random_ts);
                //Date date_occ_random = new Date(beginTime + (long) (Math.random() * diff));

		long tempValue = randInt(1,129600);
		String userID = "user" + tempValue;

		//Date date_occ_random = new Date(date_rptd_random_ts - tempValue);
		
		String userName = userNameArray[randInt(0,9)];
		/*
                DateFormat df = new SimpleDateFormat("MM/dd/yyyy");
		DateFormat timeformat = new SimpleDateFormat("hhmm");
		Date crime_date = new Date();
		String crime_date_str = df.format(crime_date);
		String crime_time_str = timeformat.format(crime_date);
                */
		writer.append(userID);
                writer.append(',');
 	        writer.append(userName);
                writer.append(',');
                writer.append(location1_random);
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
