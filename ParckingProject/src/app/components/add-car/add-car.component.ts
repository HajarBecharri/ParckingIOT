import { Component } from '@angular/core';
import { MatriculeModel } from './car.module';
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
 
  user!:UserModule;
  code_matricule!: string;
  nom_client!: string;
  cni_client!: string;
  date_enregistrement!: Date | null;
  etat!: string;

  constructor(private carservice:CarService,private router:Router,private userservice:UserService){
    userservice.userObservable.subscribe((newuser)=>
    this.user=newuser)

  }


  //event bindding
  
  saveMe(){

    

    let mycar = new MatriculeModel() ;

    mycar.code_matricule = this.code_matricule ;
    mycar.cni_client = this.cni_client ;
    mycar.nom_client = this.nom_client ;
    mycar.date_enregistrement = new Date();
    

    this.carservice.saveCare(mycar).subscribe();
    this.router.navigateByUrl("home")

  }




}

