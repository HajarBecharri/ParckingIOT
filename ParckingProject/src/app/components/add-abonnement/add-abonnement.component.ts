import { Component } from '@angular/core';
import { AbonnementModel } from './abonnement.module';
import { CarService } from '../../services/car.service';
import { Router } from '@angular/router';
import { UserModule } from '../user/user.module';
import { UserService } from 'src/app/services/user.service';
import { DatePipe } from '@angular/common';

@Component({
  selector: 'app-add-abonnement',
  templateUrl: './add-abonnement.component.html',
  styleUrls: ['./add-abonnement.component.css']
})
export class AddAbonnementComponent {
  user!: UserModule;
  code_matricule!: string;
  jours!: number;

  constructor(private carService: CarService, private router: Router, private userService: UserService) {
    userService.userObservable.subscribe((newuser)=>
    this.user=newuser)
  }

  saveAbonnement() {
    if(!isNaN(this.jours)&& this.jours>0){
      const currentdate=new Date()
      const expiration =new Date(currentdate.setDate(currentdate.getDate()+this.jours))
      const nouvelAbonnement: AbonnementModel = {
    
      date_expiration: expiration.toISOString(),
      code_matricule: this.code_matricule
    };

    this.carService.addAbonnement(nouvelAbonnement).subscribe(
      response => {
        console.log('Abonnement ajouté avec succès', response);
        this.router.navigateByUrl('home');  // Rediriger vers la page d'accueil après l'ajout
      },
      error => {
        console.error('Erreur lors de l\'ajout de l\'abonnement', error);
      }
    );
    }
    else {
      
    }
   
  }
}

