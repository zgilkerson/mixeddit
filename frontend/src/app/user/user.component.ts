import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroupDirective, FormGroup, Validators } from '@angular/forms';

import { MatSnackBar } from '@angular/material';

import { SpotifyService } from '../spotify.service';
import { MixedditError } from '../mixeddit-error';
import { trigger, transition, style, animate } from '@angular/animations';

@Component({
  selector: 'app-user',
  templateUrl: './user.component.html',
  styleUrls: ['./user.component.css'],
  providers: [SpotifyService],
  animations: [
    trigger('showSuccess', [
      transition(':leave', [
        animate(2000, style({
          opacity: 0
        }))
      ])
    ])
  ]
})
export class UserComponent implements OnInit {
  mixedditForm: FormGroup;
  loading = false;
  replaceSuccess = false;
  replaceMessage = '';
  sortBy = ['hot', 'new', 'rising', 'controversial', 'top'];
  timeFilter = [{ value: 'hour', viewValue: 'past hour' },
               { value: 'day', viewValue: 'past 24 hours' },
               { value: 'week', viewValue: 'past week' },
               { value: 'month', viewValue: 'past month' },
               { value: 'year', viewValue: 'past year' },
               { value: 'all', viewValue: 'all time' }];

  constructor(private fb: FormBuilder, private spotify: SpotifyService,
              public snackBar: MatSnackBar) {
    this.createForm();
    this.toggleCreatePublic();
    this.toggleTimeFilter();
  }

  ngOnInit() {}

  toggleCreatePublic() {
    this.mixedditForm.controls.create_playlist.valueChanges.forEach(
      (value: boolean) => {
        if (value) {
          this.mixedditForm.controls.create_public.enable();
        } else {
          this.mixedditForm.controls.create_public.disable();
        }
      }
    );
  }

  toggleTimeFilter() {
    this.mixedditForm.controls.sort_by.valueChanges.forEach(
      (value: string) => {
        if (value === this.sortBy[3] || value === this.sortBy[4]) {
          this.mixedditForm.controls.time_filter.enable();
        } else {
          this.mixedditForm.controls.time_filter.disable();
        }
      }
    );
  }

  onSubmit(formDirective: FormGroupDirective) {
    this.loading = true;
    this.replaceSuccess = false;
    console.log(this.mixedditForm.value);
    this.spotify.putPlaylistReplace(this.mixedditForm.value).subscribe(
      (data) => {
        this.loading = false;
        this.replaceSuccess = true;
        this.replaceMessage = data['playlist'] + ' has been updated using r/' + data['subreddit'];
        setTimeout(() => {
          this.replaceSuccess = false;
        }, 3000);
        formDirective.resetForm();
        this.mixedditForm.controls.sort_by.setValue(this.sortBy[4]);
        this.mixedditForm.controls.time_filter.setValue(this.timeFilter[2].value);
        this.mixedditForm.controls.limit.setValue(100);
      },
      (error: MixedditError) => {
        this.loading = false;
        if (error.message.toLowerCase().includes('subreddit')) {
          this.mixedditForm.get('subreddit').setErrors({ 'invalidSubreddit': true });
        } else if (error.message.toLowerCase().includes('playlist')) {
          this.mixedditForm.get('playlist').setErrors({ 'invalidPlaylist': true });
        } else {
          this.snackBar.open(
            'Sorry there was a problem creating the playlist',
            'Okay', {
              duration: 5000,
            });
        }
      }
    );
  }

  createForm() {
    this.mixedditForm = this.fb.group({
      subreddit: ['', Validators.required],
      sort_by: [this.sortBy[4]],
      time_filter: [this.timeFilter[2].value],
      limit: [100, [Validators.required, Validators.min(10), Validators.max(250)]],
      playlist: ['', Validators.required],
      create_playlist: [false],
      create_public: [{value: false, disabled: true}],
    });
  }
}
