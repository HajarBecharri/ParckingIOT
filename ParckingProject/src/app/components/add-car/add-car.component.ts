import { Component } from '@angular/core';
import { CarModule } from './car.module';
import { CarService } from '../../services/car.service';
import { Router } from '@angular/router';
import { UserModule } from '../user/user.module';
import { UserService } from 'src/app/services/user.service';

@Component({
  selector: 'app-add-car',
  templateUrl: './add-car.component.html',
  styleUrls: ['./add-car.component.css']
})
export class AddCarComponent {
  // two way binding
  model!:string ;

  hp!:number ;

  marque!:string ;
  user!:UserModule

  constructor(private carservice:CarService,private router:Router,private userservice:UserService){
    userservice.userObservable.subscribe((newuser)=>
    this.user=newuser)

  }


  //event bindding
  
  
  saveMe(){

    

    let mycar = new CarModule() ;

    mycar.id_car = 0 ;
    mycar.hp = this.hp ;
    mycar.model = this.model ;
    mycar.marque = this.marque ;

    this.carservice.saveCare(mycar).subscribe();
    this.router.navigateByUrl("home")

  }




}

