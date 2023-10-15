/**
 * Program Name: api interface
 * Function: API interface definition for communicating with the backend
 */
import axios from "axios";

//Questionnaire Designer Operations
export const designOpera = data => {
  return axios.post("/api/design", data).then(res => res.data);
};

//Questionnaire Respondent Actions
export const answerOpera = data => {
  return axios.post("/api/answer", data).then(res => res.data);
};
