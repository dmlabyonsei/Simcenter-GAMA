model NewAgent

global {
	file shapefile_roads <- file("../roads.shp");
	bool EarthQuake <- false;
	float proba_detect_Earthquake <- 0.01;
	float proba_detect_fear <- 0.1;
	float other_distance <- 10.0#m;
	int earthquakestart <- 100;
	bool earthquakeNotification <- false;
	int nb_know_earthquake <- 0;
	int nb_evacuated;
	int nb_adult <- 200;
	int nb_elderly <- 100;
	int nb_leader <- 100;
	
	float elderly_speed <- 0.7;
	float speaker_distance <- 100.0#m;
	file shapefile_shelters <- file("../shelters.shp");
	file shapefile_speakers <- file("../speakers.shp");
	
	int nb_people <- nb_adult + nb_elderly + nb_leader;
	int nb_people_evacuated;
	int nb_people_evacuatedN;
	int nb_adult_evacuated <-0;
	int nb_elderly_evacuated <-0;
	int nb_leader_evacuated <-0;
	int nb_people_know;
	
	geometry shape <- envelope(shapefile_roads);
	graph road_network;
	
	init {
		create road from: shapefile_roads;
		road_network <- as_edge_graph(road);
		
		create adult number: nb_adult{
			
			do add_desire(at_target);
			do add_desire(nonEarthquake ,0.0);
			
			location <- any_location_in(one_of(road));
			
			charisma<-rnd(1.0);
			receptivity<-rnd(1.0);
			
			
		}
		create elderly number: nb_elderly{
			
			do add_desire(at_target);
			do add_desire(nonEarthquake ,0.0);
			
			location <- any_location_in(one_of(road));
			
			charisma<-rnd(1.0);
			receptivity<-rnd(1.0);
			
			
		}
		create leader number: nb_leader{
			
			do add_desire(at_target);
			do add_desire(nonEarthquake ,0.0);
			
			location <- any_location_in(one_of(road));
			
			charisma<-rnd(1.0);
			receptivity<-rnd(1.0);
			
			
		}
		create earthquake number: 1;
		
		create shelter from: shapefile_shelters with: [capacity::int(read("capacity"))]{
			current_capacity <- capacity;
		}
		
		create speaker from: shapefile_speakers;
		
		
		nb_people_evacuated <- 0;
		nb_people_evacuatedN <- nb_people;
		

	}
	
	
	reflex Earthquake when: cycle = earthquakestart { EarthQuake <- true;}
	reflex earthquakeNotification when: cycle = 600 { 
		//proba_detect_Earthquake <- 1;
		//earthquakeNotification <- true;
		
	}
	
	reflex evacuated when: every(#cycle){
		
		//nb_people_evacuated <- nb_people - length(people);
		nb_people_evacuatedN <- nb_people - nb_people_evacuated;
		}
		
}

species earthquake{
	geometry shape <- rectangle(300#km, 300#km);
	bool earthquakeOccured <-false;
	rgb color <- #white;
	
	aspect default{ draw square(300#km) color: color; }
		
	reflex Earthquake when: EarthQuake = true { earthquakeOccured <- true;}
	reflex Earthquake when: EarthQuake = true {
		color <- #red;
		}
	}


species people skills: [moving] control: simple_bdi{
	
	float speed <-rnd(1.0)*1.2+1.4#m/#s;
	rgb color <- #black;
	point target;
	bool noTarget <- true;
	bool escape_mode <- false;
	bool fearful;
	bool safe <- false;
	
	bool use_emotions_architecture <- true;
	
	predicate at_target <- new_predicate("at_target");
	predicate in_shelter <- new_predicate("shelter");
	
	predicate earthquakeP <- new_predicate("earthquake");
	predicate nonEarthquake <- new_predicate("earthquake",false);
	
	emotion fearConfirmed <- new_emotion("fear_confirmed",earthquakeP);
	emotion fear <- new_emotion("fear",earthquakeP);
	
	rule emotion:fearConfirmed remove_intention: at_target new_desire:in_shelter strength:5.0;
	
	rule belief:new_predicate("earthquake") remove_intention:at_target new_desire:in_shelter strength:5.0;
	
	
	rule emotion:new_emotion("fear" ,new_predicate("earthquake")) new_desire:in_shelter remove_intention:at_target when: fearful strength:5.0;
	
	
	perceive target: earthquake when: not escape_mode and flip(proba_detect_Earthquake) and EarthQuake = true {
		focus id:"earthquake" is_uncertain: true;	
		ask myself {
			
			
			
			if(flip(proba_detect_fear)){
				fearful<-true;
			}else{
				fearful <- false;
			}
			
			do add_uncertainty(earthquakeP);
			if(fearful){
				
				do to_escape_mode;
				nb_people_know <- nb_people_know +1;
				
			}else{
				color<-rgb(204,102,0);
			}
		}
	}
	
	
	reflex notifying when : earthquakeNotification = true {
			do add_belief(earthquakeP);
			nb_know_earthquake <- nb_know_earthquake+1;
			if(not escape_mode){
				do to_escape_mode;
				nb_people_know <- nb_people_know +1;
		}
	}
	
	perceive target:speaker in: speaker_distance when: EarthQuake = true and not escape_mode{
		
		ask myself{
			do add_belief(earthquakeP);
			do to_escape_mode;
			nb_people_know <- nb_people_know +1;
		}
		
	}
	 
	perceive target:earthquake when: not escape_mode and flip(proba_detect_Earthquake) and EarthQuake = true and color = #green {
		focus id:"earthquake";
		ask myself{
			
			do add_belief(earthquakeP);
			if(not escape_mode){
				do to_escape_mode;
				nb_people_know <- nb_people_know +1;
			}
		}
	}
	
	/*
	perceive target:earthquake when: earthquakeNotification = true {
		focus id:"earthquake";
		ask myself{
			
			do add_belief(earthquakeP);
			if(not escape_mode){
				do to_escape_mode;
			}
		}
	}
	*/
	
	perceive target:people in: other_distance when: not escape_mode {
		
		ask myself{
			if(flip(0.01)){
				fearful<-true;
				
			}else{
				fearful <- false;
			}
		}
		
		emotional_contagion emotion_detected:fearConfirmed when: fearful;
		unconscious_contagion emotion:new_emotion("fear") charisma: charisma receptivity:receptivity;
		conscious_contagion emotion_detected:fearConfirmed emotion_created:fear;
	}
	
	
	
	plan normal_move intention: at_target  {
		if (target = nil) {
			target <- any_location_in(one_of(road));
		} else {
			do goto target: target on: road_network recompute_path: false;
			if (target = location)  {
				target <- nil;
				noTarget<-true;
			}
		}
	}
	
	
	
	plan evacuation intention: in_shelter {
		color <-#darkred;
		if (target = nil or noTarget) {
			 

				
			target <- (shelter with_min_of (each.location distance_to location) ).location;
				
		
			
			//target <- one_of(shelter).location;
			noTarget <- false;
		}
		else  {
			do goto target: target on: road_network recompute_path: false;
				
				if (target = location)  {
					ask shelter where (each.location = target){
						if(current_capacity = 0){
							//myself.target <- any_location_in(one_of(road));
							myself.noTarget <- true;
						}
						else{
							current_capacity <- current_capacity-1;
							nb_people_evacuated <- nb_people_evacuated +1;
							myself.safe <- true;
							
						}
					}
				}
		}
	}
	reflex dying when: safe = true{
		
		do die;
		
	}
	
	action to_escape_mode {
		escape_mode <- true;
		color <- #purple;
		target <- nil;	
		noTarget <- true;
		do remove_intention(at_target, true);
	}
	
	
	
}

species adult parent: people{
	
	reflex counting when: safe = true{
		nb_adult_evacuated <- nb_adult_evacuated +1;
	}
	
	aspect default{
		draw square(20#m) rotate: heading +90 color: color;
	}
}

species elderly parent: people{
	
	float speed <-(rnd(1.0)*1.2+1.4#m/#s) * elderly_speed;
	
	reflex counting when: safe = true{
		nb_elderly_evacuated <- nb_elderly_evacuated +1;
	}
	
	aspect default{
		draw circle(10#m) rotate: heading +90 color: color;
	}
}
species leader parent: people{
	
	reflex counting when: safe = true{
		nb_leader_evacuated <- nb_leader_evacuated +1;
	}
	
	aspect default{
		draw triangle(20#m) rotate: heading +90 color: color;
	}
}

species shelter{
	
	int capacity;
	int current_capacity;
	
	aspect default{
		draw circle(50#m) color: #red;
		
	}
	
	aspect capacity{
		draw circle(50#m) color: #red;
		draw string(current_capacity) size: 5#m color: #black ;
	}
}

species speaker{
	
	aspect default{
		draw circle(speaker_distance#m) color: #green;
	}
}

species notification{
	
	geometry shape <- rectangle(0.5#km, 0.5#km);
	bool notifying <-false;
	
	reflex Notification when: earthquakeNotification = true { notifying <- true;}
	
}

species road {
	
	//Capacity of the road considering its perimeter
	float capacity <- 1;
	//Number of people on the road
	int nb_people <- 0 update: length(people at_distance 1) max: 3;
	//Speed coefficient computed using the number of people on the road and the capicity of the road
	float speed_coeff <- 1 update:  exp(-nb_people/capacity) min: 0.1;
	
	aspect default {
		draw shape color: #black;
	}
	aspect info {
		draw (shape+speed_coeff + 3 * nb_people) color: #black;
	}
}

experiment NewAgent type: gui {
	/** Insert here the definition of the input and output of the model */
	output {
		display video1 type: opengl{
			
			species earthquake transparency: 0.9;
			species adult;
			species elderly;
			species leader;
			species road aspect: default;
			species shelter aspect: default;
			species speaker transparency: 0.5;
			
			
			}
			
		display video2 refresh: every(#cycles) {
			chart "CITY EVACUATION" type: series {
				data "Not Evacuated" value: nb_people_evacuatedN color: #red;
				data "Adult Evacuated" value: nb_adult_evacuated color: #green;
				data "Elderly Evacuated" value: nb_elderly_evacuated color: #blue;
				data "Leader Evacuated" value: nb_leader_evacuated color: #black;
			}
		}
	
		display video3 refresh:every(#cycle) type: opengl{
			species shelter aspect: capacity;
			species road;
		}
		
		display video4 refresh:every(5#cycle) {
			chart"Evacuated Percentage" type: pie background: #white{
				data  "People evacuated" value:nb_people_evacuated color: #red ;
				data  "People perceived" value:nb_people_know color: #blue ;
				data  "Not evacuated" value:nb_people_evacuatedN color: #black ;
			}
		} 
		 
		
}

}	






