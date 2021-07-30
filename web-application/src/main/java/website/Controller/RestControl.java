package website.Controller;

import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

import REST.Controller.RestClient;
import website.model.FullData;

@RestController
public class RestControl {
	RestClient rest = new RestClient();
	
	@PostMapping("/gradient")
	  FullData fullData(@RequestBody FullData newData) {
	    return rest.postGps(newData);
	  }
}
