import { Injectable } from '@angular/core';
import { Subject } from 'rxjs/Subject';

@Injectable()
export class LightsService {

  // Observable boolean source
  private lightSource = new Subject<boolean>();

  // Observable boolean stream
  lights$ = this.lightSource.asObservable();

  changeLight(lightSwitch: boolean) {
    this.lightSource.next(lightSwitch);
  }

  constructor() { }
}
