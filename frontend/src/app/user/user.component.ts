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

  constructor(private fb: FormBuilder, private spotify: SpotifyService,
              public snackBar: MatSnackBar) {
    this.createForm();
  }

  ngOnInit() {}

  onSubmit(formDirective: FormGroupDirective) {
    this.loading = true;
    this.replaceSuccess = false;
    this.spotify.putPlaylistReplace(this.mixedditForm.value).subscribe(
      (data) => {
        this.loading = false;
        this.replaceSuccess = true;
        setTimeout(() => {
          this.replaceSuccess = false;
        }, 2000);
        formDirective.resetForm();
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
      playlist: ['', Validators.required]
    });
  }
}
