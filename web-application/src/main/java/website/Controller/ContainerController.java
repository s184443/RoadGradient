package website.Controller;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.Reader;
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

import javax.validation.Valid;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.validation.BindingResult;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.multipart.MultipartFile;

import com.opencsv.bean.CsvToBean;
import com.opencsv.bean.CsvToBeanBuilder;

import REST.Controller.RestClient;
import website.model.Container;
import website.model.Data;
import website.model.FullData;
import website.repository.ContainersRepository;

@Controller
public class ContainerController {
	
	RestClient rest = new RestClient();
	
	@Autowired
	private ContainersRepository repository;
	
	@GetMapping("/")
	public String index(Model model) {
		model.addAttribute("containers", repository.findAll());
		return "index";	
	}
	
	@GetMapping("/add")
	public String add(Container container, Model model) {
		return "add";
	}
	
	@PostMapping("/add")
	public String add(@Valid Container container, BindingResult result, Model model) {
		if(result.hasErrors()) {
			return "add";
		}
		
		repository.save(container);
		return "redirect:/";
		
	}
	
	@GetMapping("/delete/{id}")
	public String delete(@PathVariable("id") long id, Model model) {
		Optional<Container> c = repository.findById(id);
		if (c.isPresent()) {
			Container cont = c.get();
			repository.delete(cont);
		}
		return "redirect:/";
	}
	
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
                	double time = Float.parseFloat(att[0]);
                	double longitude = Float.parseFloat(att[1]);
                	double latitude = Float.parseFloat(att[2]);
                	List<Double> x = new ArrayList<Double>();
                	x.add(longitude);
                	x.add(latitude);
                	fullDataList.add(x);
//                	System.out.println(fullDataList);
//                	Data data = new Data(time,longitude,latitude);
//                	fullList.add(data);
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
