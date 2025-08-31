<<<<<<< HEAD
# Deep-search-project
This is my deep search agentic project and it deals with medical ,tour and basic users querry .
In this project we have our head agent , which has three sub-agent -> greeting-medical-agent, travel-agent and helpful assistant .
# Greeting_medical_agent
greeting-medical-agent deals with all medical related querries . greeting-medical-agent has three sub-agents which are medical-expert ,medical_search_agent and backend_agent .
our  medical_expert agent deals with basic medical related querries .if the user is asking basic medical question or need to know any medical disease .The head agent 
will handoff to greeting-medical-agent which will handoff to medical_expert agent .
If the user want to know any information which needs web-search then we have medical_search_agent ,which searches the web and then give you the response .forexample user needs to know about the top hospitals in karachi ,our greeting_medical_agent will handoff to medical_search_agent .
when the user want to book an appoinment in any hospital or need to know what are the doctors available in your database/hospital then to deal with this our greeting medical-agent will handoff to backend_agent which have tools like appoinment tool and doctor_finder tool .
# Trave_agent 
The head agent has travel agent which deals with travel related querry . The travel agent has two sub-agents ,tour_guide or tour_planner agent.
if the user querry is about basic tour related so our travel-agent will handoff to our tour guide but when the user is asking about what are the famous hotels in 
karachi which needs web search ,then it is handoff to travel-planner-agent which has travel_planner_web_search .
# helpful assistant 
This is the agent will deals with querries other than medical and tour . forexample the user is planning to book a family-trip to australia .For this he needs to 
know about the cities of australia or the neighbour countries of australia . now this question cannot be replied by medical agent nor tour agent so to solve this we have
our third agent which is helpful assistant which deals with these basic neutral problems .

=======
# Deep-search-project
>>>>>>> 686d554de88554386c9b8c2d19bc368bfc095ef3
