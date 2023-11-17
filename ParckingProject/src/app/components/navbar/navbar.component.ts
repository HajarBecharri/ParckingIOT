import { Component } from '@angular/core';
import { UserModule } from '../user/user.module';
import { UserService } from 'src/app/services/user.service';
import { ActivatedRoute, Router } from '@angular/router';

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.css']
})
export class NavbarComponent {

  user!:UserModule
  constructor(private userservice:UserService,private activatedRouter:ActivatedRoute,
    private router:Router){
      userservice.userObservable.subscribe((newuser)=>
      this.user=newuser)

  }


  
  logout(){
    this.userservice.logout()
  }

}
