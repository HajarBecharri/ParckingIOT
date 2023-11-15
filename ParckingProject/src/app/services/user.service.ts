import { Injectable } from '@angular/core';

import { BehaviorSubject, Observable,tap } from 'rxjs';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { User } from '../user';
import { CarModule } from '../components/add-car/car.module';
import { UserModule } from '../components/user/user.module';
import { Router } from '@angular/router';


@Injectable({
  providedIn: 'root'
})
export class UserService {
  url:string = "http://127.0.0.1:5000";
  private userSubject= new BehaviorSubject<UserModule>(this.getusertFromLocalStorage());
  public userObservable:Observable<UserModule> ;

  httpOptions = {
    headers: new HttpHeaders({ 'Content-Type': 'application/json' })
  };

  constructor(private http:HttpClient,private router:Router) {
    this.userObservable=this.userSubject.asObservable();
   }
getdata():Observable<User[]>{
return this.http.get<User[]>('http://127.0.0.1:5000/data')
}
login(user:UserModule):Observable<UserModule>{
  console.log(user)
  return this.http.post<UserModule>(this.url+"/login" , user , this.httpOptions ).pipe(
    tap({
      next:(user)=>{
           this.setusertolocalstorage(user)
           this.userSubject.next(user);
           
      },
      error:(errorResponse)=>{
       console.log(errorResponse)
      }
    })
   )
;
    }

    private setusertolocalstorage(user:UserModule){
      localStorage.setItem('hajar',JSON.stringify(user))
             
     }
  
     private getusertFromLocalStorage():UserModule{
         const userJson=localStorage.getItem('hajar');
         if(userJson) return JSON.parse(userJson) as UserModule;
         return new UserModule();
  
     }

     logout(){
      this.userSubject.next(new UserModule());
      localStorage.removeItem('hajar');
    //to refresh the page
    
      this.router.navigateByUrl('')

     }
  
}

