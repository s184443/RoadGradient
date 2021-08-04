package REST.Controller;

import java.util.Arrays;

import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.web.client.RestTemplate;
import website.model.FullData;

public class RestClient {
	private static final String GET_GRADIENT = "http://127.0.0.1:5000/gradient";

	static RestTemplate restTemplate = new RestTemplate();
	
	public FullData postGps(FullData fullData) {
	
		HttpHeaders headers = new HttpHeaders();
		headers.setAccept(Arrays.asList(MediaType.APPLICATION_JSON));
		
//		FullData fullData = new FullData(data);
		FullData fullData2 = restTemplate.postForObject(GET_GRADIENT, fullData, FullData.class);
//		System.out.println(fullData2.getGps());
		return fullData2;
	}
}
