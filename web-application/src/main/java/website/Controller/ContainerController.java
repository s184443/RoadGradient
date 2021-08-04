package website.Controller;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.List;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.multipart.MultipartFile;

import REST.Controller.RestClient;
import website.model.Data;
import website.model.FullData;

@Controller
public class ContainerController {
	
	RestClient rest = new RestClient();
	
	
	
    @PostMapping("/upload-csv-file")
    public String uploadCSVFile(@RequestParam("file") MultipartFile file, Model model) {

        // validate file
        if (file.isEmpty()) {
            model.addAttribute("message", "Please select a CSV file to upload.");
            model.addAttribute("status", false);
        } else {

            // parse CSV file to create a list of `User` objects
            try (BufferedReader reader = new BufferedReader(new InputStreamReader(file.getInputStream()))) {

                String st;
                String[] att = {};
                List<List<Double>> fullDataList = new ArrayList<List<Double>>();
                List<Data> fullList = new ArrayList<Data>();
                while ((st = reader.readLine()) != null) {
                	att = st.split("\\s+");
                	double longitude = Float.parseFloat(att[1]);
                	double latitude = Float.parseFloat(att[2]);
                	List<Double> x = new ArrayList<Double>();
                	x.add(longitude);
                	x.add(latitude);
                	fullDataList.add(x);

                }
                FullData fullData = rest.postGps(new FullData(fullDataList));
                List<List<Double>> dataPoints = fullData.getGps();
                for (int i=0 ; i < dataPoints.size() ; i++){
                	List<Double> point = dataPoints.get(i);
                	Data data = new Data(point.get(0),point.get(1),point.get(2),point.get(3));
                	fullList.add(data);
                }
                
                // save users list on model
                model.addAttribute("data", fullList);
                model.addAttribute("status", true);

            } catch (Exception ex) {
                model.addAttribute("message", "An error occurred while processing the CSV file.");
                model.addAttribute("status", false);
            }
        }

        return "file-upload-status";
    }
}
