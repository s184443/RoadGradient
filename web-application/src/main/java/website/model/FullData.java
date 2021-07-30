package website.model;

import java.util.ArrayList;
import java.util.List;

import com.fasterxml.jackson.annotation.JsonProperty;

public class FullData {
	
	@JsonProperty("gps")
	private List<List<Double>> gps = new ArrayList<List<Double>>();
	private ArrayList<Double> speed = new ArrayList<Double>();
	private ArrayList<ArrayList<Double>> acc = new ArrayList<ArrayList<Double>>();

	public List<List<Double>> getGps() {
		return gps;
	}

	public void setGps(List<List<Double>> gps) {
		this.gps = gps;
	}

	public FullData() {
		
	}

	public FullData(List<List<Double>> gps) {
		this.gps = gps;
	}
	

}
