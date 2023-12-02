import { Component } from '@angular/core';

import { UserService } from 'src/app/services/user.service';
import { User } from 'src/app/user';
import { UserModule } from './user.module';
import { Observable } from 'rxjs';
import { Router } from '@angular/router';

@Component({
  selector: 'app-user',
  templateUrl: './user.component.html',
  styleUrls: ['./user.component.css']
})
export class UserComponent  {
 
  password!:number ;

  email!:string ;
  
  log!:any
  err=false

  


  constructor(private userservice:UserService,private router:Router){


  }


  //event bindding
  
  
  login(){

    

    let user = new UserModule() ;

    
    user.password = this.password ;
    user.email = this.email ;
    

    this.userservice.login(user).subscribe(data=>{
     
      if(data.token)
      this.router.navigateByUrl("home")
      else this.err=true
    });
    

  }



}
