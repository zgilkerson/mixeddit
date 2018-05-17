import { Component, OnInit, OnDestroy } from '@angular/core';
import { Subscription } from 'rxjs/Subscription';

import { LightsService } from '../lights.service';

@Component({
  selector: 'app-guest',
  templateUrl: './guest.component.html',
  styleUrls: ['./guest.component.css'],
})
export class GuestComponent implements OnInit, OnDestroy {
  lights = false;
  lightsSubscription: Subscription;

  constructor(private lightsService: LightsService) {
    this.lightsSubscription = lightsService.lights$.subscribe(
      lights => {
        this.lights = lights;
      }
    );
  }
  ngOnInit() {
  }

  ngOnDestroy() {
    this.lightsSubscription.unsubscribe();
  }
}
