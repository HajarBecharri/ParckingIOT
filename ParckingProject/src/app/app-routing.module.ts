import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AddCarComponent } from './components/add-car/add-car.component';
import { HomeComponent } from './components/home/home.component';
import { UserComponent } from './components/user/user.component';
import { EnregistrementComponent } from './components/enregistrement/enregistrement.component';
import { ListCarsComponent } from './components/list-cars/list-cars.component';
import { AddAbonnementComponent } from './components/add-abonnement/add-abonnement.component';
import { ParckingComponent } from './components/parcking/parcking.component';
const routes: Routes = [
{path:"home" , component:HomeComponent},
{path:"" , component:UserComponent},
{ path: 'add-car', component: AddCarComponent },
{ path: 'enregistrement', component: EnregistrementComponent },
{ path: 'list-cars', component: ListCarsComponent },
{ path: 'add-abonnement', component: AddAbonnementComponent },
{ path: 'parcking', component: ParckingComponent  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
