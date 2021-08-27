
model Evac_Agent

global {
	geometry shape <- rectangle(10, 10);
	predicate normal_desire <- new_predicate("normal");
	
	geometry moving <- rectangle(100000,100000);
	
	int nb_adult <-100;
	
	int nb_elderly <- 50;
	
	int nb_leader <- 30;
	
	init {

		create adult number: nb_adult
		{	
      	}

      	create elderly number: nb_elderly
      	{
		}
		
      	create leader number: nb_leader
      	{
			
		}
      	
      }
      
}
	

 
species people skills: [moving] control: simple_bdi{
	point target;
	float speed;
	rgb color <- #black;
	bool escape_mode <- false;
	bool normal;
	bool noTarget<-true;
	
	
	init{
		do add_desire(normal_desire );
	}
	
	plan normal_move intention: normal_desire {
		do wander speed: 0.07#km/#h amplitude:10000 bounds:moving;
	}
	/*
	plan normal_move intention: normal_desire {
		if (target = nil or noTarget)
		{
			target <- any_location_in(square(10));
			noTarget <- false;
			
		}
		else
		{
			do goto target: target;
			if(target = location) {
				target <- nil;
				noTarget <- true;
			}
		}
	}
 	
 	
 	*/
}

species adult parent: people{
	
	float speed <- 0.005 #km/#h;
	
	aspect default {
		draw square(0.2) rotate: heading + 90 color: color;
	}
}

species elderly parent: people{
	
	float speed <- 0.005 #km/#h;
	
	aspect default {
		draw circle(0.1) color: color;
	}
}

species leader parent: people{
	
	float speed <- 0.005 #km/#h;
	
	aspect default {
		draw triangle(0.2) color: color rotate: heading + 90;
	}
}

experiment NewAgent type: gui {
	output {
		display main type: opengl  {
			
			species adult refresh: true;
			species elderly refresh: true;
			species leader refresh: true;
		}
	}
}

