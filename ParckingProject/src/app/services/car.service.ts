import { Injectable } from '@angular/core';

import { MatriculeModel } from '../components/add-car/car.module';
import { Observable } from 'rxjs';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { EnregistrementModel } from '../components/enregistrement/enregistrement.module';
import { AbonnementModel } from '../components/add-abonnement/abonnement.module';

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

    return this.http.post(this.url+"/add_car" , matricule , this.httpOptions );

  }
  getAllcars():Observable<MatriculeModel[]>{

     return  this.http.get<MatriculeModel[]>(this.url+"/get_cars" ,this.httpOptions );
  }
  getParckingcars():Observable<MatriculeModel[]>{

    return  this.http.get<MatriculeModel[]>(this.url+"/get_cars_in_parking" ,this.httpOptions );
 }
  getenregistrements():Observable<EnregistrementModel[]>{

  return  this.http.get<EnregistrementModel[]>(this.url+"/get_enregistrements" ,this.httpOptions );
}
  
  delete(id:number){
    return this.http.get(this.url+"/deletecar/"+id );
  }

  update(car:MatriculeModel){
    return this.http.post(this.url+"/updatecar",car );
  }

  addAbonnement(abonnement: AbonnementModel): Observable<any> {
    return this.http.post(this.url + "/save_abonnement", abonnement, this.httpOptions);
  }





 
}

