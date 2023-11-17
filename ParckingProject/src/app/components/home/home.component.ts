import { Component } from '@angular/core';
import { MatriculeModel } from '../add-car/car.module';
import { CarService } from '../../services/car.service';
import { ActivatedRoute, Router } from '@angular/router';
import { UserModule } from '../user/user.module';
import { UserService } from 'src/app/services/user.service';

export interface PeriodicElement {
  name: string;
  position: number;
  weight: number;
  symbol: string;
}


@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent {
  
  
  user!:UserModule
  constructor(private userservice:UserService,private activatedRouter:ActivatedRoute,
    private router:Router){
      userservice.userObservable.subscribe((newuser)=>
      this.user=newuser)

  }

  
  
}

