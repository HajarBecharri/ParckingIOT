import { Injectable } from '@angular/core';

import { CarModule } from '../components/add-car/car.module';
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


  saveCare(car:CarModule){

    return this.http.post(this.url+"/savecar" , car , this.httpOptions );

  }
  getAllcars():Observable<CarModule[]>{

     return  this.http.get<CarModule[]>(this.url+"/cars" ,this.httpOptions );
  }
  
  delete(id:number){
    return this.http.get(this.url+"/deletecar/"+id );
  }

  update(car:CarModule){
    return this.http.post(this.url+"/updatecar",car );
  }



 
}

