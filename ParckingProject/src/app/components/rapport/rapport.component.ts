import { Component } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { CarService } from 'src/app/services/car.service';
import { EnregistrementModel } from '../enregistrement/enregistrement.module';

@Component({
  selector: 'app-rapport',
  templateUrl: './rapport.component.html',
  styleUrls: ['./rapport.component.css']
})
export class RapportComponent {
  title = 'Enregistrements de Matricule :  ';
  enregistremnts!:EnregistrementModel[];
  displayedColumns: string[] = ['numero enregistrement','Numero matricule', 'date entree','date sortie'];
  dataSource!:EnregistrementModel[]
  codeMatricule: string | null = null;
  
  constructor(private myservice:CarService,private activatedRouter:ActivatedRoute,
    private router:Router){
    this.codeMatricule = this.activatedRouter.snapshot.paramMap.get('codeMatricule');
    this.title=this.title+=this.codeMatricule
    this.myservice.getenregistrements().subscribe(
  
        (data)=>{
          this.enregistremnts = data.filter(
            (data) => data.code_matricule.toLowerCase().includes(this.codeMatricule!.toLowerCase())
          );
          this.dataSource = this.enregistremnts;
          
        }
  
  
    );
  }

}
