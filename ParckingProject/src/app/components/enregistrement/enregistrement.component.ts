import { Component } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { CarService } from 'src/app/services/car.service';
import { EnregistrementModel } from './enregistrement.module';

@Component({
  selector: 'app-enregistrement',
  templateUrl: './enregistrement.component.html',
  styleUrls: ['./enregistrement.component.css']
})
export class EnregistrementComponent {
  title = 'les Enregistrements ';
  enregistremnts!:EnregistrementModel[];
  displayedColumns: string[] = ['numero enregistrement','Numero matricule', 'date entree','date sortie'];
  dataSource!:EnregistrementModel[]
  codeMatricule: string | null = null;
  
  constructor(private myservice:CarService,private activatedRouter:ActivatedRoute,
    private router:Router){
    this.myservice.getenregistrements().subscribe(
  
        (data)=>{
          
          this.dataSource = data;
          
        }
  
  
    );
  }

}



