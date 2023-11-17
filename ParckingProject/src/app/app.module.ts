import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { UserComponent } from './components/user/user.component';
import { FormsModule } from '@angular/forms';
import {HttpClientModule} from '@angular/common/http';
import { HomeComponent } from './components/home/home.component';
import { AddCarComponent } from './components/add-car/add-car.component';
import{BrowserAnimationsModule} from '@angular/platform-browser/animations'
import {MatButtonModule} from '@angular/material/button';
import {MatFormFieldModule} from '@angular/material/form-field';
import {MatInputModule} from '@angular/material/input';
import {MatIconModule} from '@angular/material/icon';
import {MatCardModule} from '@angular/material/card';
import { MatTableModule } from '@angular/material/table' ;
import {MatDialogModule} from '@angular/material/dialog';
import{MatToolbarModule} from '@angular/material/toolbar';
import{MatMenuModule}from '@angular/material/menu';
import {MatDatepickerModule} from '@angular/material/datepicker';
import{MatNativeDateModule} from '@angular/material/core';
import{MatRadioModule} from '@angular/material/radio';
import {MatSelectModule} from '@angular/material/select';
import {MatSlideToggleModule} from '@angular/material/slide-toggle';
import { NavbarComponent } from './components/navbar/navbar.component';
import { ListCarsComponent } from './components/list-cars/list-cars.component';
import { EnregistrementComponent } from './components/enregistrement/enregistrement.component';
import { AddAbonnementComponent } from './components/add-abonnement/add-abonnement.component';
import { ParckingComponent } from './components/parcking/parcking.component';
import { RapportComponent } from './components/rapport/rapport.component';





@NgModule({
  declarations: [
    AppComponent,
    AddCarComponent,
    HomeComponent,
    UserComponent,
    NavbarComponent,
    ListCarsComponent,
    EnregistrementComponent,
    AddAbonnementComponent,
    ParckingComponent,
    RapportComponent,
    
  ],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    AppRoutingModule,
    FormsModule,
    HttpClientModule,
    MatButtonModule,
    MatFormFieldModule,
    MatInputModule,
    MatIconModule,
    MatCardModule,
    MatTableModule,
    MatDialogModule,
    MatToolbarModule
    
    
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
