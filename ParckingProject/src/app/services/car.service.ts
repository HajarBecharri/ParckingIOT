import { Injectable } from '@angular/core';

import { MatriculeModel } from '../components/add-car/car.module';
import { Observable } from 'rxjs';
import { HttpClient, HttpHeaders } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class CarService {
  url:string = "http://127.0.0.1:5000";

  httpOptions = {
    headers: new HttpHeaders({ 'Content-Type': 'application/json' })
  };

  constructor(private http:HttpClient) { }


  saveCare(matricule:MatriculeModel){

    return this.http.post(this.url+"/savecar" , matricule , this.httpOptions );

  }
  getAllcars():Observable<MatriculeModel[]>{

     return  this.http.get<MatriculeModel[]>(this.url+"/cars" ,this.httpOptions );
  }
  getParckingcars():Observable<MatriculeModel[]>{

    return  this.http.get<MatriculeModel[]>(this.url+"/carsInParking" ,this.httpOptions );
 }
  
  delete(id:number){
    return this.http.get(this.url+"/deletecar/"+id );
  }

  update(car:MatriculeModel){
    return this.http.post(this.url+"/updatecar",car );
  }



 
}

