package REST.Controller;

import java.util.ArrayList;
import java.util.Arrays;

import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpMethod;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.reactive.function.client.WebClient;
import org.springframework.web.reactive.function.client.WebClient.RequestBodySpec;
import org.springframework.web.reactive.function.client.WebClient.RequestHeadersSpec;
import org.springframework.web.reactive.function.client.WebClient.UriSpec;

import website.model.FullData;

public class RestClient {
	private static final String GET_GRADIENT = "http://127.0.0.1:5000/gradient";
	
	static RestTemplate restTemplate = new RestTemplate();
	
//	public static void main(String[] args) {
//		getGradient();
//		postGps();
//		
//	}
	
	public static void getGradient() {
		HttpHeaders headers = new HttpHeaders();
		headers.setAccept(Arrays.asList(MediaType.APPLICATION_JSON));
		
		HttpEntity<String> entity = new HttpEntity<>("parameters", headers);
		
		ResponseEntity<String> result = restTemplate.exchange(GET_GRADIENT, HttpMethod.GET, entity, String.class);
		System.out.println(result);
	}
	
	public FullData postGps(FullData fullData) {
//		ArrayList<ArrayList<Double>> data = new ArrayList<ArrayList<Double>>();
//		ArrayList<Double> list1 = new ArrayList<Double>();
//		ArrayList<Double> list2 = new ArrayList<Double>();
//		list1.add(55.722858428955078125);
//		list1.add(12.53600978851318359375);
//		list2.add(55.722888946533203125);
//		list2.add(12.5358104705810546875);
//		data.add(list1);
//		data.add(list2);
//		
		HttpHeaders headers = new HttpHeaders();
		headers.setAccept(Arrays.asList(MediaType.APPLICATION_JSON));
		
//		FullData fullData = new FullData(data);
		FullData fullData2 = restTemplate.postForObject(GET_GRADIENT, fullData, FullData.class);
//		System.out.println(fullData2.getGps());
		return fullData2;
	}
}
